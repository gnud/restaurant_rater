from . import utils
from . import models

from rest_framework import serializers


class RestaurantSerializer(serializers.ModelSerializer):
    can_user_vote = serializers.SerializerMethodField()

    def get_can_user_vote(self, obj):
        """
        Is the user allowed to make a vote the remaining time of the day

        :param obj: models.Restaurant
        :rtype: bool
        """
        request = self.context.get('request', object)

        if not request:
            return False

        user = (
            request.user if hasattr(request, 'user') else None
        )

        if not user:
            return False

        cache_key = utils.create_vote_cache_key(request, obj)
        is_allowed_vote, total_user_votes_now = utils.can_vote(cache_key)

        return is_allowed_vote

    class Meta:
        model = models.Restaurant
        fields = (
            'pk',
            'name',
            'description',
            'address',
            'cover',
            'can_user_vote',
        )


class RestaurantResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Restaurant
        fields = (
            'pk',
            'name',
            'description',
            'address',
            'cover'
        )


class VoteResponseSerializer(serializers.ModelSerializer):
    restaurant = RestaurantResponseSerializer()

    class Meta:
        model = models.Vote
        fields = (
            'pk',
            'restaurant',
            'created',
            'points',
        )
