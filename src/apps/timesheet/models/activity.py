from django.db import models
from .activity_type import ActivityType

from ...core.behaviors import Timestampable, Authorable
class Activity(Timestampable, Authorable):
    activity_name = models.CharField(max_length=20)
    activity_type = models.ForeignKey(ActivityType, on_delete=models.CASCADE, null=True, related_name='activity_set')


    def __str__(self):
        return self.activity_name
