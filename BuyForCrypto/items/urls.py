from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('items/', views.items, name='items'),
    path('items/<int:item_id>/', views.detail, name='item-detail'),
    path('profile/', views.detail, name='profile'),
    path('items/add_to_card/<int:item_id>/', views.add_to_card, name = 'add-to-card'),

]