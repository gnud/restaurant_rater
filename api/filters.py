from django_filters import rest_framework as filters

from api import models


class VotesFilter(filters.FilterSet):
    created = filters.DateFilter(field_name='created', lookup_expr='date')

    class Meta:
        model = models.Vote
        fields = [
            "created",
        ]
