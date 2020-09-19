import json

from django.test import TestCase
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.test import APIRequestFactory

from PizzaPoll.views import PizzaViewSet, StatsViewSet
from .models import Pizza


class PizzaTestCase(TestCase):
    def setUp(self) -> None:
        Pizza.objects.create(name='Hawaii', toppings=4)
        Pizza.objects.create(name='Cappriciosa', toppings=3)
        Pizza.objects.create(name='Salami', toppings=3)
        self.factory = APIRequestFactory()

    def test_stats_viewset(self):
        """Tests content of StatsViewSet"""
        request = self.factory.get("")
        stats_detail = StatsViewSet.as_view({'get': 'list'})
        response = stats_detail(request)

        # test response status
        self.assertEqual(response.status_code, HTTP_200_OK)

        # test response content
        response.render()
        data = json.loads(response.content)
        for raw_pizza in data:
            pizza = Pizza(name=raw_pizza['name'], toppings=raw_pizza['toppings'], votes=raw_pizza['votes'],
                          id=raw_pizza['id'])
            self.assertIn(pizza, Pizza.objects.all())

    def test_pizza_viewset(self):
        """Tests content of PizzaViewSet"""
        request = self.factory.get("")
        pizza_detail = PizzaViewSet.as_view({'get': 'list'})
        response = pizza_detail(request)

        # test response status
        self.assertEqual(response.status_code, HTTP_200_OK)

        # test response content
        response.render()
        data = json.loads(response.content)
        for raw_pizza in data:
            pizza = Pizza(name=raw_pizza['name'], toppings=raw_pizza['toppings'], id=raw_pizza['id'])
            self.assertIn(pizza, Pizza.objects.all())

    def test_cast_vote_valid(self):
        request = self.factory.post('/cast_vote/', data={'id': '1'})
        pizza_detail = PizzaViewSet.as_view({'post': 'cast_vote'})
        response = pizza_detail(request)

        # test response status
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_cast_vote_invalid(self):
        invalid_votes = [
            {'pizza': '1'},
            {},
            {'id': ''},
            {'id': 'aaaaa'}
        ]

        pizza_detail = PizzaViewSet.as_view({'post': 'cast_vote'})

        for data in invalid_votes:
            request = self.factory.post('/cast_vote/', data=data)
            response = pizza_detail(request)
            self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
