from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from api.mixins import TimeStampMixin


class Restaurant(TimeStampMixin):

    # Fields
    name = models.CharField(max_length=160)
    description = models.TextField()
    address = models.CharField(max_length=35)
    cover = models.ImageField(upload_to='restaurant_covers')

    # Relationship Fields
    # TDC...

    class Meta:
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"

    def __str__(self):
        return f'{self.name or self.pk}'


class Vote(models.Model):

    # Fields
    points = models.DecimalField(default=settings.DEFAULT_OTHER_POINTS, decimal_places=2, max_digits=4)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    # Relationship Fields
    restaurant = models.ForeignKey(
        'api.Restaurant',
        on_delete=models.CASCADE, related_name="votes",
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE, related_name="user_votes",
    )
