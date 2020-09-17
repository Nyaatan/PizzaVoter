from django.db import models


class Pizza(models.Model):
    name = models.CharField(max_length=100)
    toppings = models.IntegerField(verbose_name='Amount of toppings', default=0)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name
