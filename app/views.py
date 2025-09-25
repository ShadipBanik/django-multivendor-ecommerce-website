import traceback

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Min, Max, Avg
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import request
from django.template.loader import render_to_string

from .admin import Product_Images
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate, login as auth_login

from .helper.ProductReviewForm import ProductReviewForm
from .helper.forms import RegisterForm
from .models import Slider, Banner_area, Category, MainCategory, Product, ProductReview
from django.contrib.auth.decorators import login_required

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
        "get_absolute_url":product.get_absolute_url(),
        "additional_info": [{'specification':info.specification,'detail':info.detail} for info in product.additional_information_set.all()],
        "images":[img.images.url for img in product.product_image_set.all()] # if you have related ProductImage model
    }
    return JsonResponse(data)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.all().order_by("-created_at")
    avg_rating = product.reviews.aggregate(avg=Avg("rating"))["avg"] or 0
    review_count = product.reviews.count()
    form = ProductReviewForm(request.POST)
    if request.method == "POST":
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data["rating"]
            review_text = form.cleaned_data["review"]

            review, created = ProductReview.objects.update_or_create(
                product=product,
                user=request.user,
                defaults={
                    "rating": rating,
                    "review": review_text,
                }
            )

            if created:
                messages.success(request, "✅ Your review has been added successfully!")
            else:
                messages.info(request, "✏️ Your review was updated successfully!")

            return redirect(product.get_absolute_url())
    else:
        form = ProductReviewForm()



    context = {
        "product": product,
        "reviews": reviews,
        "avg_rating": avg_rating,
        "review_count": review_count,
        "form": form,
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
            return redirect('home')     # change to your home/dashboard
        else:
            messages.error(request, "Email or password incorrect")
            return redirect("register")

    return render(request, "account/register.html")

def logout_view(request):
    logout(request)  # Clears the session and logs out the user
    return redirect('home')

@login_required(login_url='register')
def my_profile(request):
    return render(request, "account/my-profile/profile.html")

def about_us(request):
    return render(request, "main/about-us.html")

def contact_us(request):
    return render(request, "main/contact.html")

def all_product(request):
    try:
        categories = MainCategory.objects.annotate(
            product_count=Count('categories__subcategories__product')
        )

        products = Product.objects.all().order_by('-created_at')

        # category filter (single)
        cat_id = request.GET.get("cat-item")

        if cat_id:
            products = products.filter(categories__category__main_category_id=cat_id)

        # price filter
        min_price = request.GET.get("min_price")
        max_price = request.GET.get("max_price")
        print("DEBUG received:", min_price, max_price)

        if min_price and max_price:
            try:
                min_price = int(min_price)
                max_price = int(max_price)
                if min_price > 0 or max_price > 0:
                    products = products.filter(price__gte=min_price, price__lte=max_price)
            except ValueError:
                print("DEBUG: invalid min/max price")
                pass

        print("DEBUG queryset:", products)
        print("DEBUG price range:", products.aggregate(Min("price"), Max("price")))

        # per-page filter
        per_page = request.GET.get("per_page", 2)
        try:
            per_page = int(per_page)
        except ValueError:
            per_page = 1

        paginator = Paginator(products, per_page)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "categories": categories,
            "page_obj": page_obj,
            "cat_id": cat_id,
            "per_page": per_page,
        }

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            products_html = render_to_string("pages/partials/_product_list.html", context, request=request)
            pagination_html = render_to_string("pages/partials/_pagination.html", context, request=request)
            return JsonResponse({
                "products_html": products_html,
                "pagination_html": pagination_html,
            })

        return render(request, "pages/product.html", context)

    except Exception as e:
        return JsonResponse({"error": str(e), "traceback": traceback.format_exc()}, status=500)