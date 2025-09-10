from django.contrib import admin

from . models import *
# Register your models here.

class Product_Images(admin.TabularInline):
      model = Product_Image

class Addtional_Informations(admin.TabularInline):
      model = Additional_Information

class Product_Admin(admin.ModelAdmin):
      inlines = (Product_Images,Addtional_Informations)
      list_display = ('product_name','price','categories', 'section')
      list_editable = ('price','categories', 'section')



admin.site.register(Slider)
admin.site.register(Banner_area)
admin.site.register(MainCategory)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Section)
admin.site.register(Product,Product_Admin)
admin.site.register(Product_Image)
admin.site.register(Additional_Information)
