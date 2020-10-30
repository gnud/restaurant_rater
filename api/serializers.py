from . import models

from rest_framework import serializers


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Restaurant
        fields = (
            'pk',
            'name',
            'description',
            'address',
            'cover',
        )
