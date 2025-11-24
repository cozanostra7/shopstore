#Quick overview
#Tech stack
Python + Django

Django REST Framework (DRF)

rest_framework_nested for nested routes

SQLite/Postgres (any Django-supported DB)

Image uploads (Django ImageField) — make sure MEDIA_ROOT is configured

Uses Django models, ModelViewSets, serializers, and DRF permissions
#What it includes
Models: Product, Collection, Promotion, Customer, Cart, CartItem, Order, OrderItem, Review, ProductImage, Address

Serializers: Model serializers and custom serializers for cart and order flows

Views: ModelViewSet + nested routers for reviews and cart items

Business logic: add-to-cart merging, create order from cart with DB transaction, prevent deleting products used in orders, prevent deleting collections with products

Validators & signals: validate_file_size (image file validator) and order_created signal hook (project contains signals.py referenced)

#Installation & setup

git clone https://github.com/cozanostra7/shopstore
cd shopstore
cd storefront
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
