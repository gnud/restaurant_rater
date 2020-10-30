from django.db import models

from api.mixins import TimeStampMixin


class Restaurant(TimeStampMixin):
    name = models.CharField(max_length=160)
    description = models.TextField()
    address = models.CharField(max_length=35)
    cover = models.ImageField(upload_to='restaurant_covers')

    class Meta:
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"

    def __str__(self):
        return f'{self.name or self.pk}'
