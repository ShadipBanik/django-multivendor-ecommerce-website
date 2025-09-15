from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import request
from .admin import Product_Images
from django.contrib.auth import login
from django.contrib.auth import authenticate, login as auth_login
from .helper.forms import RegisterForm
from .models import Slider, Banner_area, Category, MainCategory,Product

def index(request):
    sliders = Slider.objects.all().order_by('-id')[0:3]
    banners = Banner_area.objects.all().order_by('-id')[0:3]
    products = Product.objects.filter(section__name = 'Top Deals Of The Day')
    print(products)
    context = {
        "sliders": sliders,
        "banners": banners,
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
        "discount": product.discount,
        "tags": product.tags,
        "additional_info": [{'specification':info.specification,'detail':info.detail} for info in product.additional_information_set.all()],
        "images":[img.images.url for img in product.product_image_set.all()] # if you have related ProductImage model
    }
    return JsonResponse(data)


def product_detail(request, slug):
    product = Product.objects.filter(slug=slug)

    if product.exists():
        print('exist')
        product = Product.objects.get(slug=slug)
    else:
        print('not exist')
        return  redirect("not_found_404")

    main_category = MainCategory.objects.all()[0:10]
    context = {
        "product": product,
        "main_category": main_category,
    }

    return render(request, "pages/product_detail.html",context)

def not_found_404(request):
    return render(request, "error/404.html")

def my_account(request):
    return render(request, "account/register.html")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            login(request, user)
            messages.success(request, "Account created successfully")
            return redirect("register")  # redirect where you want
    else:
        form = RegisterForm()
    return render(request, "account/register.html", {"form": form})


def hlogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Email or password incorrect")
            return redirect("register")

        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            auth_login(request, user)   # ✅ use Django’s login
            return HttpResponse('Ok')     # change to your home/dashboard
        else:
            messages.error(request, "Email or password incorrect")
            return redirect("register")

    return render(request, "account/register.html")
