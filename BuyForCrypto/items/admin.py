from django.contrib import admin
from .models import Category, Subcategory, Item, Review
# Register your models here.

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Item)
admin.site.register(Review)

