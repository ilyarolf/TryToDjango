import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Item, Review, Category, Subcategory
from django.views.generic import DetailView
# Create your views here.


def index(request):
    return render(request, 'items/index.html')


def detail(request, item_id):
    # return HttpResponse(request, f'{item_id}')
    item = Item.objects.get(pk=item_id)
    return render(request, 'items/item_detail_view.html', {"item": item})


def items(request):
    items = Item.objects.all()
    return render(request, 'items/items.html', {"items" : items})

def add_to_cart(request, item_id):
    user_cart = request.COOKIES.get('user_cart')
    if user_cart is None:
        cookies = f'{item_id}_END_'
    else:
        cookies = f'{user_cart}{item_id}_END_'
    response = HttpResponseRedirect('/items')
    expire_date = datetime.datetime.now()
    expire_date = expire_date + datetime.timedelta(days=7)
    response.set_cookie(key='user_cart', value = cookies,expires=expire_date)
    return response

def profile(request):
    pass

def cart(request):
    user_cart = request.COOKIES.get('user_cart')
    if user_cart is None:
        return render(request, 'items/cart.html', {'user_cart': None})
    else:
        id_in_cart = user_cart.split('_END_')
        items_list = []
        for id in id_in_cart:
            try:
                items_list.append(Item.objects.get(pk = id))
            except:
                pass
        return render(request, 'items/cart.html', {'user_cart': items_list})

def del_from_cart(request, item_id):
    user_cart = request.COOKIES.get('user_cart')
    if user_cart is not None:
        cookies = user_cart.replace(f'{item_id}_END_', '')
        response = HttpResponseRedirect('/cart')
        expire_date = datetime.datetime.now()
        expire_date = expire_date + datetime.timedelta(days=7)
        response.set_cookie(key='user_cart', value=cookies, expires=expire_date)
        return response

def categories(request):
    categories_list = Category.objects.all()
    return render(request, 'items/categories.html', {'categories_list' : categories_list})

def show_category(request, category_id):
    items = Item.objects.filter(item_category=category_id)
    return render(request, 'items/items.html', {"items" : items})
