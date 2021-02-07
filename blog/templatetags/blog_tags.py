from ..models import Post, Category
from django import template

register = template.Library()

@register.simple_tag
def get_post(num=5):
    return Post.objects.all().order_by('-created')[:num]

@register.simple_tag
def archives():
    return Post.objects.dates('created', 'month', order='DESC')

@register.simple_tag
def get_categories():
    return Category.objects.all()