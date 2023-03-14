from django.db import models

# Create your models here.


class Item(models.Model):
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
    review_rating = models.IntegerField('Рейтинг отзыва')
    review_description = models.CharField(max_length=250)

    def __str__(self):
        return self.review_rating

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

