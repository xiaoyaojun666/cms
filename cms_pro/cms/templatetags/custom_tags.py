from django import template

register = template.Library()

@register.filter
def paginator_url(page_number, number):
    return f'?page={number}'