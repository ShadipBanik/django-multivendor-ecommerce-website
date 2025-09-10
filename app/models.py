from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

class Slider(models.Model):

      discount_deal_options = {
          ('HOT DEALS','HOT DEALS'),
          ('New Arraivels','New Arraivels'),
          ('New DEALS', 'New DEALS')

      }

      image = models.ImageField(upload_to='media/slider')
      discount_deal = models.CharField(choices=discount_deal_options, max_length=100)
      sale = models.IntegerField()
      brand_name = models.CharField(max_length=100)
      discount = models.IntegerField()
      link = models.CharField(max_length=100)


      def __str__(self):
          return self.brand_name

class Banner_area(models.Model):
      image = models.ImageField(upload_to='media/banner')
      discount_deal = models.CharField(max_length=100)
      qoute = models.CharField(max_length=100)
      discount = models.IntegerField()
      link = models.CharField(max_length=100,null=True)


      def __str__(self):
          return self.qoute

class MainCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    main_category = models.ForeignKey(
        MainCategory, on_delete=models.CASCADE, related_name="categories"
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.main_category.name} → {self.name}"


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="subcategories"
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category.main_category.name} → {self.category.name} → {self.name} →"


class Section(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
      total_quantity = models.IntegerField()
      available_quantity = models.IntegerField()
      featured_image = models.ImageField(upload_to='media/product')
      product_name = models.CharField(max_length=100)
      price = models.IntegerField()
      discount = models.IntegerField()
      product_information = RichTextField()
      model_name = models.CharField(max_length=100)
      categories = models.ForeignKey(
        Category, on_delete=models.CASCADE
      )
      tags = models.CharField(max_length=100)
      description = RichTextField()
      section = models.ForeignKey(Section, on_delete=models.DO_NOTHING)
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)

      def __str__(self):
          return self.product_name

class Product_Image(models.Model):
      product = models.ForeignKey(
        Product, on_delete=models.CASCADE
      )
      images = models.ImageField(upload_to='media/product',default='')


class Additional_Information(models.Model):
      product = models.ForeignKey(
        Product, on_delete=models.CASCADE
      )
      specification = models.CharField(max_length=100)
      detail = models.CharField(max_length=100)

