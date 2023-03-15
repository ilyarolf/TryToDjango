from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('items/', views.items, name='items'),
    path('items/<int:item_id>/', views.detail, name='item-detail'),
    path('profile/', views.detail, name='profile'),
    path('items/add_to_cart/<int:item_id>/', views.add_to_cart, name = 'add-to-cart'),
    path('cart/', views.cart, name='cart'),
    path('cart/del/<int:item_id>/', views.del_from_cart,name = 'del-from-cart'),
    path('categories/', views.categories, name = 'categories'),
    path('categories/<int:category_id>/', views.show_category, name = 'show-category'),
]