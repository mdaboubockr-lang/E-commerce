from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('address/create/', views.address_create, name='address_create'),
    path('address/', views.address_list, name='address_list'),
    path('address/update/<int:pk>/', views.address_update, name='address_update'),
    path('address/delete/<int:pk>/', views.address_delete, name='address_delete'),
]
