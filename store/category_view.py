from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from typing import Optional, List
from dataclasses import dataclass
from django.db.models.query import QuerySet
from store.models import Category, Product, ProductTags
from django.core.paginator import Paginator
from django.views.generic.list import ListView
from django.utils.http import urlencode
from typing import Dict, Any, List


@dataclass
class FilterParams:
    """Data class to hold filter parameters"""
    query: Optional[str] = None
    sort_by: Optional[str] = None
    price: Optional[int] = None
    tag_id: Optional[int] = None

    @classmethod
    def from_request(cls, request) -> 'FilterParams':
        return cls(
            query=request.GET.get('q'),
            sort_by=request.GET.get('sort'),
            price=request.GET.get('price'),
            tag_id=request.GET.get('tag')
        )


class ProductQuerySetMixin:
    """Mixin for optimized product querysets"""

    def get_base_queryset(self) -> QuerySet:
        return Product.objects.select_related(
        ).prefetch_related(
            'categories',
            'tag',
        ).filter(
            is_available=True
        )


class CategoryQuerySetMixin:
    """Mixin for optimized category querysets"""

    def get_category_queryset(self) -> QuerySet:
        return Category.objects.select_related(
            'parent'
        ).prefetch_related(
            'children'
        )


class FilterMixin:
    """Mixin for filtering products"""
    sort_options = {
        'date_newest': '-created_at',
        'price_lowest': 'price',
        'price_high': '-price',
        'name_asc': 'name',
        'name_desc': '-name',
    }

    # IDE suggests these should be static, so I think there might be a better solution for this
    def apply_search(self, queryset: QuerySet, query: str):
        if not query:
            return queryset

        return queryset.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    def apply_price_filter(self, queryset: QuerySet, price: Optional[int]) -> QuerySet:
        if price and price.isdigit():
            return queryset.filter(price__lte=int(price))
        return queryset

    def apply_tag_filter(self, queryset: QuerySet, tag_id: Optional[int]) -> QuerySet:
        if tag_id and tag_id.isdigit():
            return queryset.filter(tag__id=int(tag_id))
        return queryset

    def apply_sorting(self, queryset: QuerySet, sort_by: Optional[str]) -> QuerySet:

        return queryset.order_by(self.sort_options.get(sort_by, '-created_at'))


class CustomPaginator(Paginator):
    """Custom paginator with additional helper methods"""

    def get_page_range(self, current_page: int, show_pages: int = 5) -> range:
        """
        Return a range of page numbers to display, centered around current page

        Args:
            current_page: Current page number
            show_pages: Number of pages to show (odd number recommended)
        """
        middle = show_pages // 2
        if self.num_pages <= show_pages:
            return range(1, self.num_pages + 1)

        if current_page <= middle + 1:
            return range(1, show_pages + 1)

        if current_page >= self.num_pages - middle:
            return range(self.num_pages - show_pages + 1, self.num_pages + 1)

        return range(current_page - middle, current_page + middle + 1)


class PaginatedListView(ListView):
    paginate_by = 9
    paginator_class = CustomPaginator
    show_pages = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'page_obj' not in context:
            return context

        context.update({
            'page_range': context['paginator'].get_page_range(
                context['page_obj'].number,
                self.show_pages
            ),
            'query_params': self.get_query_params(),
            'show_pages': self.show_pages,
        })

        return context

    def get_query_params(self):
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            del query_params['page']
        return f'&{urlencode(query_params)}' if query_params else ''


class CategoryView(PaginatedListView, ProductQuerySetMixin, CategoryQuerySetMixin, FilterMixin):
    template_name = 'shop.html'
    context_object_name = 'products'
    paginate_by = 9
    category = None

    def get_queryset(self) -> QuerySet:
        """Get filtered and sorted product queryset"""
        queryset = self.get_base_queryset()

        # Get category if specified
        category_slug = self.kwargs.get('slug')
        if category_slug:
            self.category = get_object_or_404(
                self.get_category_queryset(),
                slug=category_slug
            )
            queryset = queryset.filter(categories=self.category)
        else:
            self.category = None

        # Apply filters
        filter_params = FilterParams.from_request(self.request)

        if filter_params.query:
            queryset = self.apply_search(queryset, filter_params.query)

        queryset = self.apply_price_filter(queryset, filter_params.price)
        queryset = self.apply_tag_filter(queryset, filter_params.tag_id)
        queryset = self.apply_sorting(queryset, filter_params.sort_by)

        return queryset.distinct()

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """Get context with additional filter data"""
        context = super().get_context_data(**kwargs)
        filter_params = FilterParams.from_request(self.request)

        context['category'] = self.category
        context['subcategories'] = (
            self.category.get_children() if self.category
            else self.get_category_queryset().filter(parent__isnull=True)
        )

        # Add filter data
        context.update({
            'selected_sort': filter_params.sort_by,
            'selected_price': int(
                filter_params.price) if filter_params.price and filter_params.price.isdigit() else None,
            'selected_tag_id': int(
                filter_params.tag_id) if filter_params.tag_id and filter_params.tag_id.isdigit() else None,
            'query': filter_params.query,
            'tags': ProductTags.objects.all(),
        })

        return context
