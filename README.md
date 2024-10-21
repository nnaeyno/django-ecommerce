# django-ecommerce
E-commerce app using Django
# Django E-commerce Application

This is an early-stage Django-based e-commerce application. Currently, the app includes basic models for categories, <br>
products, and user carts, as well as HTML templates for the front end. The app structure and functionality are under <br> 
development, with plans to add more features in future iterations.

## Features

- **Category**: Products are organized into categories. Categories can have subcategories (tree structure).
- **Product**: Each product belongs to one or more categories. A product has attributes like name, description, price, image, and quantity.
- **User Cart**: Each user has a cart that stores selected products.

## Models

1. **Category**
   - `title`: Name of the category.
   - `parent`: Foreign key for subcategories (self-referential relationship).
   
2. **Product**
   - `name`: Name of the product.
   - `description`: Description of the product.
   - `price`: Price of the product.
   - `quantity`: Available quantity of the product.
   - `categories`: Many-to-many relationship with categories.
   - `created_at`: Time of creation
   - `product_image`: Image of a product
   - `is_available`: Current status of a product

   
3. **User Cart**
   - `user`: One-to-one relationship with the user.
   - `count` = Number of items
   - `total` = Total price
   - `updated` = Date of update
   - `timestamp` = Count time
   
## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ecommerce-app.git
   cd ecommerce-app

## To Do
* Add product details page.
* Implement user authentication.
* Add cart management features (add, remove, and update items).
* Add checkout and payment functionality.
* Improve HTML templates and front-end design.