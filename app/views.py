from django.shortcuts import render
from .models import Slider, Banner_area, Category, MainCategory


def index(request):
    sliders = Slider.objects.all().order_by('-id')[0:3]
    banners = Banner_area.objects.all().order_by('-id')[0:3]
    main_category = MainCategory.objects.all()[0:10]
    return render(request, "main/index.html", {"sliders": sliders,"banners": banners,'main_category':main_category})

def base(request):
    return render(request, "base.html")