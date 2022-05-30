from django.db import models

from pizza.models import Pizza


class Restaurant(models.Model):

    name = models.CharField(max_length=32)

    pizzas = models.ManyToManyField(Pizza, through="MenuEntry")

    def __str__(self):
        return self.name


class MenuEntry(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    price = models.IntegerField(null=False)
