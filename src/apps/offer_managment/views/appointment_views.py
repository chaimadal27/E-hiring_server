# python lib
import datetime
import time
import os
# django lib
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import generics, filters, status
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

# custom lib
from rest_framework.response import Response

from ..models import Appointment
from ..serializers import AppointmentSerializer
from ..exceptions import InvalidDateException
from rest_framework import views

from ...core.filters import MultiFieldsFilter

User = get_user_model()


class FilterDateRangeList(filters.SearchFilter):
    start_date_query_param = 'start'
    stop_date_query_param = 'end'
    date_field_name = 'date'

    @staticmethod
    def get_range_dates(request):
        query_params = request.query_params
        start_date_str = query_params.get(FilterDateRangeList.start_date_query_param, None)
        stop_date_str = query_params.get(FilterDateRangeList.stop_date_query_param, None)

        try:
            start_date = start_date_str and datetime.datetime.strptime(start_date_str, settings.DATE_FORMAT) or None
            stop_date = stop_date_str and datetime.datetime.strptime(stop_date_str, settings.DATE_FORMAT) or None
            return start_date, stop_date
        except ValueError:
            # TODO: TO describe exception
            raise InvalidDateException()

    def filter_queryset(self, request, queryset, view):
        start_date, end_date = FilterDateRangeList.get_range_dates(request)
        filter_kwargs = []
        if start_date:
            query = {f'{self.date_field_name}__gte': start_date}
            filter_kwargs.append(Q(**query))

        if end_date:
            query = {f'{self.date_field_name}__lte': end_date}
            filter_kwargs.append(Q(**query))

        import pprint
        pp = pprint.PrettyPrinter(depth=6)
        pp.pprint(filter_kwargs)
        return queryset.filter(*filter_kwargs)


class AppointmentCreateAPIView(generics.CreateAPIView):
    """
    Create Appointment View.
    """
    queryset = Appointment.objects.filter(deleted_at__isnull=True)
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerializer


class AppointmentsOfferListAPIView(generics.ListAPIView):
    """
    list Appointments by folder.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    filter_backends = [FilterDateRangeList]
    pagination_class = None


class AppointmentRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    list Appointments by folder.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = AppointmentSerializer
    filter_backends = [FilterDateRangeList]
    pagination_class = None
    queryset = Appointment.objects.filter(
        deleted_at__isnull=True,
    )


class MyAppointmentsListAPIView(generics.ListAPIView):
    """
    My Appointments .
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    pagination_class = None

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.filter(user=self.request.user)


class MyRecentAppointmentsListAPIView(generics.ListAPIView):
    """
    My Recent Appointments .
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    # filter_backends = [FilterDateRangeList]
    pagination_class = None

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.filter(user=self.request.user).order_by('-date')


class AppointmentsListByOfferAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    filter_backends = [FilterDateRangeList]
    pagination_class = None


class AppointementFilter(MultiFieldsFilter):
    def filter_queryset(self, request, queryset, view):
        search_terms = self.get_search_terms(request)
        conditions = self.conditions(search_terms, queryset.model)
        # if search_terms.get('email'):
        #     criterion1 = Q(candidate__first_name_fr__icontains=search_terms.get('email'))
        #     conditions.append(criterion1)
        # if search_terms.get('last_name_fr'):
        #     criterion2 = Q(candidate__last_name_fr__icontains=search_terms.get('last_name_fr'))
        #     conditions.append(criterion2)
        # if search_terms.get('first_name_fr'):
        #     criterion3 = Q(candidate__telephone__icontains=search_terms.get('first_name_fr'))
        #     conditions.append(criterion3)
        return queryset.filter(*conditions)


class AppointmentDeactivateAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.filter(
        deleted_at__isnull=True,
        # is_active=True
    )

    def perform_destroy(self, instance):
        instance.deleted_by = self.request.user
        instance.deleted_at = datetime.datetime.now()
        # instance.is_active=False
        instance.save()
