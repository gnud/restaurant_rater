from django.db import models


class TimeStampMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MultiSerializersMixin:
    def get_serializer_class(self):
        # noinspection PyUnresolvedReferences
        return self.serializer_classes.get(self.action, self.serializer_class)