"""
Models for products, categories, plans weeks, kind of plans
"""
from django.db import models


class Category(models.Model):
    """
    categories of products
    """
    class Meta:
        """
        fixed name in admin
        """
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        """
        get friendly name to show
        """
        return self.friendly_name


class Plans(models.Model):
    """
    plans days and data for every day model
    """
    class Meta:
        """
        fixed plan name in admin
        """
        verbose_name_plural = 'Plans'

    name = models.OneToOneField('Product',
                                on_delete=models.CASCADE,
                                unique=True)

    number_of_weeks = models.ForeignKey('Weeks',
                                        null=True,
                                        on_delete=models.SET_NULL)
    kind_of_plan = models.ForeignKey('TypeOfPlan',
                                     null=True,
                                     on_delete=models.SET_NULL)

    day1 = models.CharField(max_length=254, null=True, blank=True)
    day2 = models.CharField(max_length=254, null=True, blank=True)
    day3 = models.CharField(max_length=254, null=True, blank=True)
    day4 = models.CharField(max_length=254, null=True, blank=True)
    day5 = models.CharField(max_length=254, null=True, blank=True)
    day6 = models.CharField(max_length=254, null=True, blank=True)
    day7 = models.CharField(max_length=254, null=True, blank=True)


class TypeOfPlan(models.Model):
    """
    type of plans model
    """
    name = models.CharField(max_length=30)
    friendly_name = models.CharField(max_length=254,
                                     null=True,
                                     blank=True)

    def __str__(self):
        """
        str method
        """
        return self.name

    def get_friendly_name(self):
        """
        get friendly name to show
        """
        return self.friendly_name


class Weeks(models.Model):
    """
    number of weeks plans
    """
    class Meta:
        """
        fixed name in admin
        """
        verbose_name_plural = 'Weeks'

    name = models.CharField(max_length=1)
    friendly_name = models.CharField(max_length=254,
                                     null=True,
                                     blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        """
        get friendly name to show
        """
        return self.friendly_name


class Product(models.Model):
    """
    product model
    """
    category = models.ForeignKey('Category',
                                 null=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6,
                                decimal_places=2)
    rating = models.DecimalField(max_digits=6,
                                 decimal_places=2,
                                 null=True,
                                 blank=True)
    image_url = models.URLField(max_length=1024,
                                null=True,
                                blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
