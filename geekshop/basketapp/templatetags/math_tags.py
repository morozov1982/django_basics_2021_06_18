from django import template

register = template.Library()


@register.simple_tag
def multiply(num_1, num_2, *args, **kwargs):
    return num_1 * num_2
