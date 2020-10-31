from django.conf import settings
from django.core.cache import cache

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from . import models
from . import serializers
from . import utils
from .mixins import MultiSerializersMixin


class RestaurantViewSet(MultiSerializersMixin, viewsets.ModelViewSet):
    """ViewSet for the Restaurant class"""
    queryset = models.Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer
    serializer_classes = {
        'retrieve': serializers.RestaurantResponseSerializer,
        'list': serializers.RestaurantSerializer,
        'create': serializers.RestaurantResponseSerializer,
    }
    permission_classes = [permissions.IsAuthenticated]


class VoteViewSet(viewsets.ModelViewSet):
    """ViewSet for the Vote class"""
    queryset = models.Vote.objects.all()
    serializer_class = serializers.RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]


class VoteCreateVoteViewSet(viewsets.GenericViewSet):
    """ViewSet for the Vote class"""
    queryset = models.Restaurant.objects.all()
    serializer_class = serializers.VoteResponseSerializer
    permission_classes = [permissions.IsAuthenticated]

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

        cache_key = utils.create_vote_cache_key(request, restaurant_obj)

        is_allowed_vote, total_user_votes_now = utils.can_vote(cache_key)

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

        points = settings.POINTS_RULES.get(total_user_votes_now, 0.25)
        user = request.user

        vote = models.Vote.objects.create(
            restaurant=restaurant_obj,
            points=points,
            user=user,
        )

        _serializer = self.get_serializer(vote)

        return Response(data=_serializer.data)
