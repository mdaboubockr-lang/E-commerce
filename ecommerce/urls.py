from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Product import views as product_views
from Cart import views as cart_views
from Payment import views as payment_views
from Order import views as order_views
from Accounts import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', product_views.home, name='home'),
    path('shop/', product_views.product_list, name='product_list'),
    path('shop/<slug:slug>/', product_views.category_shop, name='category_shop'),
    path('', include('Accounts.urls')),
    path('product/<int:pk>/', product_views.product_detail_view, name='product_detail'),
    path('reviews/', include('Review.urls')),
    path('cart/', cart_views.cart_detail, name='cart_detail'),
    path('cart/add/', cart_views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:pk>/', cart_views.update_cart_item, name='update_cart_item'),
    path('orders/', order_views.orders, name='orders'),
    path('orders/<int:pk>/', order_views.order_detail, name='order_detail'),
    path('wishlist/', account_views.wishlist, name='wishlist'),
    path('wishlist/toggle/<int:pk>/', account_views.wishlist_toggle, name='wishlist_toggle'),
    path('password/change/', account_views.change_password, name='change_password'),
    path('payment/checkout/', payment_views.checkout, name='checkout'),
    path('payment/initiate/<int:order_id>/', payment_views.payment_initiate, name='payment_initiate'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
