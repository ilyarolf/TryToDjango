from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Item, Review
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

def add_to_card(request, item_id):
    user_cart = request.COOKIES.get('user_cart')
    if user_cart == None:
        cookies = f'{item_id}_END_'
    else:
        cookies = f'{user_cart}{item_id}_END_'
    response = HttpResponseRedirect('/items')
    response.set_cookie(key='user_cart', value = cookies)
    return response

def profile(request):
    pass
