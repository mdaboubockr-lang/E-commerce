from django.urls import path

from .views import review_create, review_update, review_delete

urlpatterns = [
    path('product/<slug:product_slug>/review/', review_create, name='review_create'),
    path('review/<int:pk>/edit/', review_update, name='review_update'),
    path('review/<int:pk>/delete/', review_delete, name='review_delete'),
]
