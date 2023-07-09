import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Item, Review, Category, Subcategory
from .utils import encode_to_base64, decode_from_base64
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm
# Create your views here.


def index(request):
    return render(request, 'items/index.html')


def detail(request, item_id):
    # return HttpResponse(request, f'{item_id}')
    item = Item.objects.get(pk=item_id)
    return render(request, 'items/item_detail_view.html', {"item": item})
@login_required
def profile(request):
    return render(request, 'items/profile.html')

def items(request):
    items = Item.objects.all()
    return render(request, 'items/items.html', {"items" : items})

def add_to_cart(request, item_id):
    category = Item.objects.filter(pk=item_id).values('item_category')[0]['item_category']
    user_cart = request.COOKIES.get('user_cart')
    if user_cart is None:
        cookies = encode_to_base64(f'{item_id}_END_')
    else:
        user_cart = decode_from_base64(user_cart)
        cookies = encode_to_base64(f'{user_cart}{item_id}_END_')
    response = HttpResponseRedirect(f'/categories/{category}')
    expire_date = datetime.datetime.now()
    expire_date = expire_date + datetime.timedelta(days=7)
    response.set_cookie(key='user_cart', value = cookies,expires=expire_date)
    return response

def cart(request):
    user_cart = request.COOKIES.get('user_cart')
    if user_cart is None:
        return render(request, 'items/cart.html', {'user_cart': None})
    else:
        user_cart = decode_from_base64(request.COOKIES.get('user_cart'))
        id_in_cart = user_cart.split('_END_')
        items_list = []
        for id in id_in_cart:
            try:
                items_list.append(Item.objects.get(pk = id))
            except:
                pass
        return render(request, 'items/cart.html', {'user_cart': items_list})

def del_from_cart(request, item_id):
    user_cart = decode_from_base64(request.COOKIES.get('user_cart'))
    if user_cart is not None:
        cookies = user_cart.replace(f'{item_id}_END_', '')
        cookies = encode_to_base64(cookies)
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

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid credentials'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'items/login.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registration_success')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def registration_success(request):
    return render(request, 'registration/registration_success.html')