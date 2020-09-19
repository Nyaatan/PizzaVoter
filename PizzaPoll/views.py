from rest_framework import mixins, status
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from .models import Pizza
from .serializers import PizzaSerializer, StatsSerializer


class PizzaViewSet(mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    ViewSet representing vote-ready list of items.

    At GET request returns available items (id, name, ammount of toppings).

    Handles vote casting via cast_vote action.
    """

    queryset = Pizza.objects.all().order_by('name')
    serializer_class = PizzaSerializer

    @action(detail=False, methods=['post'])
    def cast_vote(self, request, pk=None):
        """
        Method handling vote casting.

        Saves new vote based on data in POST request.

        Data is a dict-like object containing pair {'id': *ID*}, where *ID* is positive integer.

        :returns
        HTTP_400_BAD_REQUEST if provided data is invalid |
        HTTP_201_CREATED if vote is cast successfully
        """

        data: dict = request.data

        try:
            assert "id" in data.keys()
            assert data['id'].isdigit()
            assert len(Pizza.objects.filter(pk=int(data['id']))) > 0
        except AssertionError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        pizza = Pizza.objects.get(pk=int(data['id']))
        pizza.votes = pizza.votes + 1
        pizza.save()
        return Response(status=status.HTTP_201_CREATED)


class StatsViewSet(mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    ViewSet representing voting statistics.

    At GET request returns available items (id, name, ammount of toppings, votes)
    """

    queryset = Pizza.objects.all().order_by('-votes')
    serializer_class = StatsSerializer
