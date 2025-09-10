from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('base/', views.base, name='base'),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("product/quick-view/<int:id>/", views.product_quick_view, name="product_quick_view"),

    ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)