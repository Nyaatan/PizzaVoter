from rest_framework import serializers

from .models import Pizza


class PizzaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pizza
        fields = ('id', 'name', 'toppings')


class StatsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pizza
        fields = ('id', 'name', 'toppings', 'votes')
