# django lib
from django.db import models
from django.conf import settings

# custom lib
from apps.core.behaviors import Authorable, Timestampable
from apps.lists_managment.models import List,Option



class School(Authorable, Timestampable):
    """school"""
    short_name_fr = models.CharField(max_length=30, null=True, blank=True)
    long_name_fr = models.CharField(max_length=200, null=True, blank=True)
    short_name_ar = models.CharField(max_length=200, null=True, blank=True)
    long_name_ar = models.CharField(max_length=200, null=True, blank=True)
    web_site = models.CharField(max_length=100, blank=True, null=True)
    type = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    # is_active = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.short_name_fr} {self.long_name_fr}"

    @property
    def get_type(self):
        dict = {}
        list = List.objects.get(name="Type de l'école")
        options = Option.objects.filter(list=list).values("rank", "value")
        for option in options:
            dict[option.get("rank")] = option.get("value")
        return dict.get(self.type)

    @staticmethod
    def get_schools(ids):
        if ids:
            queryset = School.objects.filter(id__in=ids)
        else:
            queryset = School.objects.all()
        fields = settings.SCHOOL_FIELD_CONFIG_CSV
        titles = settings.SCHOOL_TITLE_CONFIG_CSV
        return queryset, fields, titles



