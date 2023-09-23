# python lib
import datetime
# django lib
from django.core.exceptions import FieldDoesNotExist
from django.db.models.fields.related import ForeignObjectRel, OneToOneRel, OneToOneField
from django.db import models
from rest_framework.settings import api_settings
from rest_framework.filters import OrderingFilter, SearchFilter
from django.db.models.constants import LOOKUP_SEP
import re
# custom lib
from apps.core.utils import camel_to_snake

class RelatedOrderingFilter(OrderingFilter):
    """
    Extends OrderingFilter to support ordering by fields in related models
    using the Django ORM __ notation
    """
    def is_valid_field(self, model, field):
        """
        Return true if the field exists within the model (or in the related
        model specified using the Django ORM __ notation)
        """
        components = field.split('__', 1)
        try:

            field = model._meta.get_field(components[0])

            if isinstance(field, OneToOneField):
                return True

            if isinstance(field, OneToOneRel):
                return self.is_valid_field(field.related_model, components[1])

            # reverse relation
            if isinstance(field, ForeignObjectRel):
                return self.is_valid_field(field.model, components[1])

            # foreign key
            if field.rel and len(components) == 2:
                return self.is_valid_field(field.rel.to, components[1])
            return True
        except FieldDoesNotExist:
            return False
    
    def remove_invalid_fields(self, queryset, fields, view, request):
        pattern = re.compile(r'(?<!^)(?=[A-Z])')
        fields = [pattern.sub('_', field.replace(".", "__")).lower() for field in fields ]
        return [term for term in fields if self.is_valid_field(queryset.model, term.lstrip('-'))]


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
