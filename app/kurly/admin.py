from django.contrib import admin

from .models import Category, Subcategory, Image, Order, OrderProduct, Option, Product


class SubcategoryInline(admin.TabularInline):
    model = Subcategory


class ProductInline(admin.TabularInline):
    model = Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        SubcategoryInline
    ]


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    inlines = [
        ProductInline
    ]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    search_fields = ['product__name']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name']
