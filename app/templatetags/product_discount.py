import math

from django import template


register = template.Library()

@register.simple_tag
def product_discount_calc(price, discount):

    if discount is None or discount is 0:
        return price

    discount_price = price-(price * discount/100)
    return math.floor(discount_price)

@register.simple_tag
def progress_bar(total,available):

       progress_bar = available
       progress_bar = available * (100/total)

       return math.floor(progress_bar)
