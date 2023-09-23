# django lib
from django.db import models
from django.conf import settings
from apps.lists_managment.models import List,Option

# custom lib
from apps.core.behaviors import Authorable, Timestampable
#from apps.core.services import retrieve_resources_by_id


class Company(Authorable, Timestampable):
    name_fr = models.CharField(max_length=30, null=True, blank=True)
    name_ar = models.CharField(max_length=30, null=True, blank=True)
    telephone = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    web_site = models.CharField(max_length=100, blank=True, null=True)
    activity = models.IntegerField(null=True, blank=True)
    address_fr = models.TextField(null=True, blank=True)
    address_ar = models.TextField(null=True, blank=True)
    staff = models.IntegerField(null=True, blank=True)
    logo = models.ImageField(upload_to="Company/logo", blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name_fr

    @property
    def get_responsable(self):
        responsable = self.contact_set.all().filter(is_principal=True).first()
        return responsable

    @property
    def get_activity(self):
        dict={}
        list=List.objects.get(name="Activity")
        options=Option.objects.filter(list=list).values("rank","value")
        for option in options:
            dict[option.get("rank")]=option.get("value")
        return dict.get(self.activity)

    @property
    def get_staff(self):
        dict = {}
        list = List.objects.get(name="Staff")
        options = Option.objects.filter(list=list).values("rank", "value")
        for option in options:
            dict[option.get("rank")] = option.get("value")
        return dict.get(self.staff)

    # @property
    # def get_legal_form(self):
    #     legal_form_dict = dict(settings.LEGAL_FORM)
    #     return legal_form_dict.get(self.legal_form)

    @staticmethod
    def get_companies(ids):
        if ids:
            queryset = Company.objects.filter(id__in=ids)
        else:
            queryset = Company.objects.all()
        fields = settings.PARTENAR_FIELD_CONFIG_CSV
        titles = settings.PARTENAR_TITLE_CONFIG_CSV
        return queryset, fields, titles

    # @property
    # def Company_type(self):
    #     Company_type_id = self.Company_type_external_id
    #     if not Company_type_id:
    #         return None
    #     Company_type = retrieve_resources_by_id(settings.Company_URL, Company_type_id)
    #     return Company_type
    #
    # @property
    # def theme(self):
    #     theme_id = self.theme_external_id
    #     if not theme_id:
    #         return None
    #     theme = retrieve_resources_by_id(settings.THEME_URL, theme_id)
    #     return theme

