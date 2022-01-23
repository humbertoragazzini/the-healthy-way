from django.db import models

# Create your models here.

class Category (models.Model):
    name = models.Charfield(max_length=254)
    friendly_name = models.Charfield(max_length=254, null=True, blank=True)

    def _str_(self)
        return self.name
    
    def get_friendly_name(self)
        return self.friendly_name

class Product_Type (models.Model):
    name = models.Charfield(max_length=254)
    friendly_name = models.Charfield(max_length=254, null=True, blank=True)
        
    def _str_(self)
        return self.name

    def get_friendly_name(self)
        return self.friendly_name

class Nutrition()
    nutrition_id =
    vegan = 


class Workout_Plans()
    dificulty
    type_objective
    duration

class Nutrition_Plans()
    dificulty
    type_objective
    vegan
    duration

class Product(model.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    product_type = models.ForeignKey('Product_Type')
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name