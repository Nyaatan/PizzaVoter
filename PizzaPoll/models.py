from django.db import models


class Pizza(models.Model):
    """
    Model of pizza in database. Contains name, amount of toppings and nomber of votes cast.
    """
    name = models.CharField(max_length=100)
    toppings = models.PositiveIntegerField(verbose_name='Amount of toppings', default=0)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.name} (ID: {self.id}, {self.toppings} toppings, {self.votes} votes)'
