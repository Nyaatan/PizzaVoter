from rest_framework import mixins, status
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from .models import Pizza
from .serializers import PizzaSerializer, StatsSerializer


class PizzaViewSet(mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Pizza.objects.all().order_by('name')
    serializer_class = PizzaSerializer

    @action(detail=False, methods=['post'])
    def cast_vote(self, request, pk=None):
        data: dict = request.data

        try:
            assert "id" in data.keys()
            assert data['id'].isdigit()
        except AssertionError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            pizza = Pizza.objects.get(pk=int(data['id']))
            pizza.votes = pizza.votes + 1
            pizza.save()
            # TODO Redirect
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)


class StatsViewSet(mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Pizza.objects.all().order_by('-votes')
    serializer_class = StatsSerializer
