from django.db import models
from django.conf import settings
# custom lib
from apps.core.behaviors import Authorable, Timestampable
from .job_category import JobCategory


class Job(Authorable, Timestampable):
    """job name"""
    name_fr = models.CharField(max_length=100, null=True, blank=True)
    name_ar = models.CharField(max_length=100, null=True, blank=True)
    # is_validated = models.BooleanField(default=False)
    status = models.IntegerField(choices=settings.JOB_STATUS, default=settings.NEW_STATUS, null=True, blank=True)
    # Foreign Keys
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name_fr} {self.description_fr}"