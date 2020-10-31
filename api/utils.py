import datetime

from constance import config
from django.core.cache import cache


def create_vote_cache_key(request, restaurant_obj):
    today_is = datetime.datetime.today().strftime('%d%m%Y')
    """
        This is allow to vote for given restaurant on daily basis for the current user 
        """
    cache_key = f'dt-{today_is}-u-{request.user.username}-r{restaurant_obj.pk}-vote'
    return cache_key


def can_vote(cache_key):
    daily_max_turns: int = config.DAILY_VOTES  # vote rules max
    total_user_votes: int = cache.get(cache_key, 0)  # past
    total_user_votes_now: int = total_user_votes + 1  # now
    is_allowed_vote = total_user_votes_now <= daily_max_turns

    return is_allowed_vote, total_user_votes_now
