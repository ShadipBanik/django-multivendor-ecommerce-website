from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.index, name='index'),
    path('base/', views.base, name='base'),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("product/quick-view/<int:id>/", views.product_quick_view, name="product_quick_view"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    # path("account/my-account", views.my_account, name="my_account"),
    path("account/register", views.register, name="register"),
    path("account/hlogin", views.hlogin, name="hlogin"),
    path("404/", views.not_found_404, name="not_found_404"),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='account/password_reset.html'),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='account/password_reset_confirm.html',
             success_url='/password-reset-complete/'  # redirect after password reset
         ),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),
         name='password_reset_complete'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)