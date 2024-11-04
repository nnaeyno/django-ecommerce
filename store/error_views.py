from django.shortcuts import render


def error_404(request, exception):
    context = {'exception': exception,
               'error_code': 404,
               'error_message': 'Page not found',
               }
    return render(request, '404.html', status=404, context=context)


def error_500(request):
    context = {
               'error_code': 500,
               'error_message': 'Server Error',
               }
    return render(request, '404.html', status=500, context=context)
