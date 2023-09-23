import datetime

from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import filters, generics, permissions, status
# function based
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.utils import export_xlsx

from ..filters import MultiFieldsFilter
from ..models.business_unit_model import BusinessUnit
from ..models.legal_agency_model import LegalAgency
from ..serializers.legal_agency_serializer import LegalAgencySerializer


class LegalAgencyListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = LegalAgency.objects.prefetch_related('business_unit_set').all()
    serializer_class = LegalAgencySerializer
    search_fields = (
        'agency_name',
        'agency_address',
        'agency_legal_status'
    )
    filter_backends = [MultiFieldsFilter, filters.OrderingFilter]
    ordering_fields = ['agency_name']
    ordering = ['pk']
    
    def filter_queryset(self, queryset):
        is_deleted = self.request.query_params.get('is_deleted', None)
        if is_deleted == '1':
            queryset = LegalAgency.objects.filter(deleted_at__isnull = False)
            return queryset
        else:
            queryset = LegalAgency.objects.filter(deleted_at__isnull = True)
            return queryset

    
    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            serializer.save(created_by = request.user, created_at = datetime.datetime.now())
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LegalAgencyListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LegalAgencySerializer
    queryset = LegalAgency.objects.all()


@api_view(http_method_names=["GET","PATCH"])
@permission_classes([permissions.IsAuthenticated])
def get_update_legal_agency(request:Request, pk:int):
    if request.method == "GET":
        legalAgency = LegalAgency.objects.prefetch_related('business_unit_set').get(pk = pk) 
        serializer = LegalAgencySerializer(instance=legalAgency)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == "PATCH":
        legalAgency = get_object_or_404(LegalAgency, pk = pk)
        serializer = LegalAgencySerializer(instance=legalAgency, data=request.data)
        if serializer.is_valid():
            serializer.save(
                    updated_by = request.user,
                    updated_at = datetime.datetime.now()
                    )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def deactivate_legal_agency(request:Request, pk: int):
    legalAgency = get_object_or_404(LegalAgency, pk = pk)
    legalAgency.deleted_at = datetime.datetime.now()
    legalAgency.deleted_by = request.user
    legalAgency.save()
    response = {
        "message":"legal agency deactivated succsefully"
    }
    return Response(data=response, status=status.HTTP_200_OK)

@api_view(http_method_names=["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def activate_legal_agency(request:Request, pk:int):
    legalAgency = get_object_or_404(LegalAgency, pk=pk)
    legalAgency.deleted_at = None
    legalAgency.deleted_by = None
    legalAgency.save()
    response = {
        "message":"legal agency activated successfully"
    }
    return Response(data=response, status=status.HTTP_200_OK)

@api_view(http_method_names=["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def deactivate_all_legal_agencies(request:Request):
    legalAgencies = LegalAgency.objects.filter(
        deleted_at__isnull = True
    )
    for item in legalAgencies:
        item.deleted_at = datetime.datetime.now()
        item.deleted_by = request.user
        item.save()
    response = {"message":"all legal agencies deactivated successfully"}
    return Response(data=response, status = status.HTTP_200_OK)


@api_view(http_method_names=["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def activate_all_legal_agencies(request:Request):
    legalAgencies = LegalAgency.objects.filter(deleted_at__isnull = False)
    for item in legalAgencies:
        item.deleted_at = None
        item.deleted_by = None
        item.save()
    response = {"message":"all legal agencies activated succsefully"}
    return Response(data = response, status = status.HTTP_200_OK)
