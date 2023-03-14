from django import template
from items.models import Item, Review

register = template.Library()

@register.simple_tag
def get_rows():
    return Item.objects.all()