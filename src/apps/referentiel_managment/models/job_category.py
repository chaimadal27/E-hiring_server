# django lib
from django.db import models
from django.conf import settings

# custom lib
from apps.core.behaviors import Authorable, Timestampable
# from apps.referentiel_managment.models import Job
#from apps.core.services import retrieve_resources_by_id


class JobCategory(Authorable, Timestampable):
    """job categories"""
    name_fr = models.CharField(max_length=100, null=True, blank=True)
    description_fr = models.TextField( null=True, blank=True)
    name_ar = models.CharField(max_length=100, null=True, blank=True)
    description_ar = models.TextField(null=True, blank=True)


    def __str__(self):
        return f"{self.name_fr} {self.description_fr}"

    # @property
    # def get_jobs(self):
    #     list = []
    #     category = JobCategory.objects.get(name_fr=self.name_fr)
    #     jobs = Job.objects.filter(category=category).values("name_fr")
    #     for option in jobs:
    #         list.append(option.get("name_fr"))
    #     return list

    @staticmethod
    def get_categories(ids):
        if ids:
            queryset = JobCategory.objects.filter(id__in=ids)
        else:
            queryset = JobCategory.objects.all()
        fields = settings.JOB_FIELD_CONFIG_CSV
        titles = settings.JOB_TITLE_CONFIG_CSV
        return queryset, fields, titles




