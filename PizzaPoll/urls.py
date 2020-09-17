from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'pizzas', views.PizzaViewSet, basename='pizzas')
router.register(r'stats', views.StatsViewSet, basename='stats')

urlpatterns = [
    path('', include(router.urls)),
]
