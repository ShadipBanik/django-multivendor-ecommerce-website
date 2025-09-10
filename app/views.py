from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from .admin import Product_Images
from .models import Slider, Banner_area, Category, MainCategory,Product


def index(request):
    sliders = Slider.objects.all().order_by('-id')[0:3]
    banners = Banner_area.objects.all().order_by('-id')[0:3]
    main_category = MainCategory.objects.all()[0:10]
    products = Product.objects.filter(section__name = 'Top Deals Of The Day')
    print(products)
    context = {
        "sliders": sliders,
        "banners": banners,
        'main_category': main_category,
        'products': products,
    }

    return render(request, "main/index.html",context )

def base(request):
    return render(request, "base.html")

def product_quick_view(request, id):
    product = Product.objects.get(id=id)
    data = {
        "id": product.id,
        "name": product.product_name,
        "price": float(product.price),  # Decimal → float
        "description": product.product_information,
        "total_quantity": product.total_quantity,
        "available_quantity": product.available_quantity,
        "model_name": product.model_name,
        "categories": product.categories.name,
        "tags": product.tags,
        "additional_info": [{'specification':info.specification,'detail':info.detail} for info in product.additional_information_set.all()],
        "images":[img.images.url for img in product.product_image_set.all()] # if you have related ProductImage model
    }
    return JsonResponse(data)