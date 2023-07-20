import asyncio
import datetime
from asgiref.sync import async_to_sync
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from items.utils.CryptoApiRequest import CryptoApiRequest

from .models import Item, Category, BuyForCryptoUser
from items.utils.utils import encode_to_base64, decode_from_base64
from items.utils.CryptoAddressGenerator import CryptoAddressGenerator
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
    user = request.user
    balance = user.top_up_amount - user.consume_amount
    return render(request, 'items/profile.html', {'balance': balance})


def items(request):
    items = Item.objects.all()
    return render(request, 'items/items.html', {"items": items})


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
    response.set_cookie(key='user_cart', value=cookies, expires=expire_date)
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
                items_list.append(Item.objects.get(pk=id))
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
    return render(request, 'items/categories.html', {'categories_list': categories_list})


def show_category(request, category_id):
    items = Item.objects.filter(item_category=category_id)
    return render(request, 'items/items.html', {"items": items})


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
            user = form.save(commit=False)
            last_user = BuyForCryptoUser.objects.last()
            if last_user is None:
                wallet_depth = 0
            else:
                wallet_depth = last_user.pk + 1
            crypto_addresses = CryptoAddressGenerator().get_addresses(wallet_depth)
            new_user = BuyForCryptoUser(
                username=user.username,
                email=user.email,
                btc_address=crypto_addresses['btc'],
                ltc_address=crypto_addresses['ltc'],
                trx_address=crypto_addresses['trx'],
            )
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            return redirect('registration_success')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def registration_success(request):
    return render(request, 'registration/registration_success.html')


def refresh_balance(request):
    user = request.user

    crypto_api_request = CryptoApiRequest()
    crypto_api_request.refresh_balances(user)

    balance = user.top_up_amount - user.consume_amount
    return render(request, 'items/profile.html', {'user': request.user, 'balance': balance})

@login_required
def buy_now(request, item_id):
    if request.method == 'POST':
        user = request.user
        balance = user.top_up_amount - user.consume_amount
        item = Item.objects.get(pk=item_id)
        if balance > item.item_price:
            user.consume_amount+=item.item_price
            user.save()
            balance = user.top_up_amount - user.consume_amount
            return render(request, 'items/profile.html', {'user': request.user, 'balance': balance})
        else:
            return render(request, 'items/profile.html', {'user': request.user, 'balance': balance})
