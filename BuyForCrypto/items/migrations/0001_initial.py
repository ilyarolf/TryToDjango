# Generated by Django 4.1.7 on 2023-03-15 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_category', models.CharField(max_length=50, verbose_name='Категория товара')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=50, verbose_name='Название товара')),
                ('item_description', models.TextField(verbose_name='Описание товара')),
                ('item_price', models.IntegerField(verbose_name='Цена')),
                ('item_picture', models.CharField(default='', max_length=150, verbose_name='Фото товара')),
                ('item_category', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='items.category')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_subcategory', models.CharField(max_length=50, verbose_name='Подкатегория товара')),
            ],
            options={
                'verbose_name': 'Подкатегория',
                'verbose_name_plural': 'Подкатегории',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_rating', models.IntegerField(verbose_name='Рейтинг отзыва')),
                ('review_description', models.CharField(max_length=250, verbose_name='Описание отзыва')),
                ('item', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='items.item')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.AddField(
            model_name='item',
            name='item_subcategory',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='items.subcategory'),
        ),
    ]
