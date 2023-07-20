from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Category(models.Model):
    category_name = models.CharField('Категория товара', max_length=50)
    category_picture = models.CharField('Изображение категории', max_length=100, default='')

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Subcategory(models.Model):
    subcategory_name = models.CharField('Подкатегория товара', max_length=50)
    subcategory_picture = models.CharField('Изображение подкатегории', max_length=100, default='')

    def __str__(self):
        return self.subcategory_name

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

class Item(models.Model):
    item_category = models.ForeignKey(Category, on_delete= models.CASCADE, default='')
    item_subcategory = models.ForeignKey(Subcategory, on_delete= models.CASCADE, default='')
    item_name = models.CharField('Название товара', max_length=50)
    item_description = models.TextField('Описание товара')
    item_price = models.IntegerField('Цена')
    item_picture = models.CharField('Фото товара', max_length=150, default='')

    def __str__(self):
        return self.item_name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Review(models.Model):
    item = models.ForeignKey(Item, on_delete= models.CASCADE, default='')
    review_rating = models.IntegerField('Рейтинг отзыва')
    review_description = models.CharField('Описание отзыва', max_length=250)

    def __str__(self):
        return str(self.review_rating)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

class BuyForCryptoUser(AbstractUser):
    email = models.CharField(error_messages={'unique': 'A user with that email already exists.'},blank=True, max_length=254, verbose_name='email address', unique=True)
    btc_address = models.CharField('Адрес BTC', max_length=40, unique=True)
    ltc_address = models.CharField('Адрес LTC', max_length=40, unique=True)
    trx_address = models.CharField('Адрес TRX', max_length=40, unique=True)
    btc_balance = models.FloatField('Баланс BTC', default=0)
    ltc_balance = models.FloatField('Баланс LTC', default=0)
    usdt_balance = models.FloatField('Баланс USDT', default=0)
    top_up_amount = models.FloatField('Сумма пополнений', default=0)
    consume_amount = models.FloatField('Сумма трат', default=0)
    last_refresh_balance_datetime = models.DateTimeField('Последнее время обновления баланса', null=True, blank=True)


    def __str__(self):
        return str(self.username)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'