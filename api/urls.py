from django.urls import path, include
from rest_framework import routers

from . import api

router = routers.DefaultRouter()
router.register(r'restaurant', api.RestaurantViewSet)
router.register(r'votes', api.VoteViewSet)
router.register(
    prefix=r'restaurant/(?P<pk>[^/]+)/vote',
    viewset=api.VoteCreateVoteViewSet,
    basename='api-v2-restaurant-vote'
)
router.register(
    prefix=r'restaurant/(?P<pk>[^/]+)/history',
    viewset=api.VoteHistoryViewSet,
    basename='api-v1-restaurant-history'
)


urlpatterns = (
    # urls for Django Rest Framework API
    path('api/v1/', include(router.urls)),
)
