from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path(
    'add-to-cart/<int:product_id>/<int:quantity>/',
    views.add_to_cart,
    name='add_to_cart'
),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('signup/', views.signup, name='signup'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.orders, name='orders'),
    path(
    'payment-success/',
    views.payment_success,
    name='payment_success'
),
    path(
    'add-review/<int:product_id>/',
    views.add_review,
    name='add_review'
),
    path(
    'add-to-wishlist/<int:product_id>/',
    views.add_to_wishlist,
    name='add_to_wishlist'
),
    path(
    'wishlist/',
    views.wishlist,
    name='wishlist'
),
    path(
    'apply-coupon/',
    views.apply_coupon,
    name='apply_coupon'
),
    path(
    'invoice/<int:order_id>/',
    views.download_invoice,
    name='download_invoice'
),
]