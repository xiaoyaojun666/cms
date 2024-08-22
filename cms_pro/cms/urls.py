from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category_items/<int:category_id>/', views.category_items, name='category_items'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('search/', views.search, name='search'),
    path('item_summary/<int:item_id>/', views.item_summary, name='item_summary'),

]