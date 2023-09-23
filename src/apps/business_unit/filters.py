import datetime

from django.core.exceptions import FieldDoesNotExist
from rest_framework.filters import SearchFilter
from django.db.models.constants import LOOKUP_SEP
from django.db import models
from rest_framework.settings import api_settings

from apps.core.utils import camel_to_snake


class MultiFieldsFilter(SearchFilter):
    """
    Extends SearchFilter to support Search by many fields in models.
    using the Django ORM.
    """

    def get_search_field_term(self, model, search_term):
        """
        Return search_term_field if the field exists within the model.
        """
        try:
            field_name, value = search_term
            field = model._meta.get_field(field_name)
            lookup = 'icontains'

            if isinstance(field, (models.fields.CharField, models.fields.TextField)):
                return LOOKUP_SEP.join([field_name, lookup]), value

            if isinstance(field, (models.fields.DateField, models.fields.DateTimeField)):
                value = datetime.datetime.strptime(value, api_settings.DATE_FORMAT).date()

            if isinstance(field, models.fields.BooleanField):
                value = value == 'true'

            return field_name, value

        except FieldDoesNotExist:
            return False, False

    def conditions(self, search_terms, model):
        orm_lookups = []
        for search_term in search_terms.items():
            key, value = self.get_search_field_term(model, search_term)
            if not key:
                continue

            orm_lookups.append(
                models.Q(**{key: value})
            )
        return orm_lookups

    def get_search_terms(self, request):
        query_params = request.query_params
        query_params_snake_case = {
            camel_to_snake(key): value for key, value in query_params.items()
        }
        import pprint
        pp = pprint.PrettyPrinter(depth=6)
        pp.pprint("*******************search terms***************************")
        pp.pprint(query_params_snake_case)
        pp.pprint("**********************************************")
        return query_params_snake_case

    def filter_queryset(self, request, queryset, view):
        search_terms = self.get_search_terms(request)
        conditions = self.conditions(search_terms, queryset.model)
        # TODO: remove this print
        import pprint
        pp = pprint.PrettyPrinter(depth=6)
        pp.pprint("********************** conditions ************************")
        pp.pprint(conditions)
        pp.pprint("**********************************************")
        return queryset.filter(*conditions)
