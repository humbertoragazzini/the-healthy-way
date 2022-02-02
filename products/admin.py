from django.contrib import admin
from .models import Product, Category, Plans, TypeOfPlan, Weeks
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )

    ordering = ('sku',)


class PlansAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'number_of_weeks',
        'kind_of_plan',
    )

    ordering = ('id',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Plans, PlansAdmin)
admin.site.register(TypeOfPlan)
admin.site.register(Weeks)
