from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

from rest_framework_nested import routers

# urlpatterns = [
#     path('products/', views.ProductList.as_view(), name='product-list'),
#     path('collections/', views.CollectionList.as_view(), name='collection-list'),
#     path('collection/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail'),
#     path('products/<int:pk>/', views.ProductDetail.as_view(), name='product-detail')
# ]

# router = DefaultRouter()
# router.register('products', views.ProductViewSet)
# router.register('collections', views.CollectionViewSet)
# urlpatterns = router.urls

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)
router.register('orders', views.OrderViewSet, basename='orders')

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')

urlpatterns = router.urls + products_router.urls + carts_router.urls

