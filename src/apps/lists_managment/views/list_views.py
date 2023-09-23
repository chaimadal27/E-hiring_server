# django lib
from contextvars import Context

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated

# custom lib
from ..serializers import ListSerialiser
from ..models import List
from ...core import models
from ..filters import MultiFieldsFilter



class ListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ListSerialiser
    permission_classes = [IsAuthenticated]
    queryset = List.objects.all()
    search_fields = (
        'name',
        'values'
    )
    filter_backends = [MultiFieldsFilter, filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['pk']





class ListRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ListSerialiser
    permission_classes = [IsAuthenticated]
    queryset = List.objects.filter(
        deleted_at__isnull=True,
    )



class AllListsListAPIView(generics.ListAPIView):
    queryset = List.objects.filter(
        deleted_at__isnull=True,
    )
    permission_classes = [IsAuthenticated]
    serializer_class = ListSerialiser
    pagination_class = None

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.filter()




class ListDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ListSerialiser
    queryset = List.objects.all()


