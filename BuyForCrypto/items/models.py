import django.contrib.auth.models
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

