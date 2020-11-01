from operator import itemgetter

from . import utils
from . import models

from django.db.models import Sum, Max, Count
from rest_framework import serializers


class RestaurantSerializer(serializers.ModelSerializer):
    can_user_vote = serializers.SerializerMethodField()
    is_winner = serializers.SerializerMethodField()

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

    @staticmethod
    def get_is_winner(obj):
        _max = (
            models.Restaurant.objects.all()
            .annotate(sum_points=Sum('votes__points'))
            .values('pk', 'sum_points')
            .aggregate(Max('sum_points'))
            .get('sum_points__max')
        )

        _total_biggest = (
            models.Restaurant.objects.all().annotate(
                sum_points=Sum('votes__points')
            )
            .filter(sum_points=_max).values('pk', 'sum_points')
        )

        _total_biggest_cnt = _total_biggest.count()

        is_tie = _total_biggest_cnt > 1

        # If one or more winners aka votes sum have the same amount, then we go checking votes by unique voters
        if is_tie:
            counts_data = {}

            for rest in _total_biggest:
                # Pity, I couldn't figure it out how to use it with filter(restaurant__in=_total_biggest)
                # instead of this ugly for loop

                rest_pk = rest.get('pk')  # current pk

                counts_data[rest_pk] = (
                    models.Vote.objects
                    .filter(restaurant=rest_pk)  # find current loop pk
                    .values('user', 'restaurant')  # only focus on these fields
                    .order_by('user')
                    .annotate(user_cnt=Count('user'))  # count how many unique users
                    .distinct()  # were found, notice this removes duplicates
                    .values_list('user', flat=True)  # we only want the ids of the unique users
                    .count()  # now we know how many unique users were voting
                )

            is_winner = (
                dict(
                    # Find the first match of dictionary view which is largest as result dictionary
                    sorted(counts_data.items(), key=itemgetter(1), reverse=True)[:1]
                )
                .get(obj.pk) is not None) or False  # get only the target row and check if has value or not as bool

            return is_winner

        return False

    class Meta:
        model = models.Restaurant
        fields = (
            'pk',
            'name',
            'description',
            'address',
            'cover',
            'can_user_vote',
            'is_winner',
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
