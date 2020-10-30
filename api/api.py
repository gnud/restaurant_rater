from . import models
from . import serializers
from rest_framework import viewsets, permissions


class RestaurantViewSet(viewsets.ModelViewSet):
    """ViewSet for the Restaurant class"""
    queryset = models.Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]
