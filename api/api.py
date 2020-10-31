import datetime

from django.core.cache import cache
from . import models
from . import serializers
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from constance import config


class RestaurantViewSet(viewsets.ModelViewSet):
    """ViewSet for the Restaurant class"""
    queryset = models.Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]


class VoteViewSet(viewsets.ModelViewSet):
    """ViewSet for the Vote class"""
    queryset = models.Vote.objects.all()
    serializer_class = serializers.RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]


class VoteCreateVoteViewSet(viewsets.GenericViewSet):
    """ViewSet for the Vote class"""
    queryset = models.Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]

    points_rules = {
        1: 1,
        2: 0.5
    }

    # noinspection PyUnusedLocal
    def create(self, request, *args, **kwargs):
        """
        Action create vote

        VOTING rules:
        1. Generate voting key based on current user, restaurant and today as date only
        2. Determine whether the user is allowed to vote
        3. Return the vote as response

        @type request: rest_framework.request.Request
        @type args: list
        @type kwargs: dict
        @rtype: rest_framework.response.Response
        """

        restaurant_obj = self.get_object()

        cache_key = self.create_cache_key(request, restaurant_obj)

        is_allowed_vote, total_user_votes_now = self.can_vote(cache_key)

        if not is_allowed_vote:
            return Response(
                data={'error': 'Vote limit reached'},
                # https://tools.ietf.org/html/rfc6585 "429 Too Many Requests" useful for limiting access
                status=status.HTTP_429_TOO_MANY_REQUESTS,
                headers={
                    # Inform the users that they can use it the next day
                    'Retry-After': 60 * 60 * 24
                }
            )

        cache.set(cache_key, total_user_votes_now)

        points = self.points_rules.get(total_user_votes_now, 0.25)
        user = request.user

        vote = models.Vote.objects.create(
            restaurant=restaurant_obj,
            points=points,
            user=user,
        )

        _serializer = self.get_serializer_vote(vote)

        if not _serializer:
            # Skip update if primary category
            return Response([{
                'error': _serializer.errors,
            }], status=status.HTTP_400_BAD_REQUEST)

        return Response(data=_serializer.data)

    @staticmethod
    def get_serializer_vote(instance):
        _serializer = serializers.VoteSerializer(data={}, instance=instance)

        if not _serializer.is_valid(raise_exception=False):
            return None

        return _serializer

    @staticmethod
    def create_cache_key(request, restaurant_obj):
        today_is = datetime.datetime.today().strftime('%d%m%Y')
        """
            This is allow to vote for given restaurant on daily basis for the current user 
            """
        cache_key = f'dt-{today_is}-u-{request.user.username}-r{restaurant_obj.pk}-vote'
        return cache_key

    @staticmethod
    def can_vote(cache_key):
        daily_max_turns: int = config.DAILY_VOTES  # vote rules max
        total_user_votes: int = cache.get(cache_key, 0)  # past
        total_user_votes_now: int = total_user_votes + 1  # now
        is_allowed_vote = total_user_votes_now <= daily_max_turns

        return is_allowed_vote, total_user_votes_now
