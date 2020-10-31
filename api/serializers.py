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


class VoteSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer(read_only=True)

    class Meta:
        model = models.Vote
        fields = (
            'pk',
            'restaurant',
            'created',
            'points',
        )
