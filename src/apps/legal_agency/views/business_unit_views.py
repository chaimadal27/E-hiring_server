import datetime
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import generics, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from ..filters import MultiFieldsFilter
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.http import Http404

from ..models.business_unit_model import BusinessUnit
from ..serializers.business_unit_serializer import BusinessUnitSerializer





@api_view(http_method_names=["GET","POST"])
@permission_classes([permissions.IsAuthenticated])
def list_create_business_units(request:Request):
    if request.method == "GET":
        is_deleted = request.query_params.get('is_deleted')
        if is_deleted == '1':
            businessUnits = BusinessUnit.objects.filter(deleted_at__isnull = False)
            serializer = BusinessUnitSerializer(instance=businessUnits, many = True)
            response = {
                    "message":"business units that are deleted",
                    "results":serializer.data
                    }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            businessUnits = BusinessUnit.objects.filter(deleted_at__isnull = True)
            serializer = BusinessUnitSerializer(instance=businessUnits, many=True)
            response = {
                    "message":"business units that are not deleted",
                    "results":serializer.data
                    }
            return Response(response, status=status.HTTP_200_OK)
    if request.method == "POST":
        serializer = BusinessUnitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                    created_by = request.user,
                    created_at = datetime.datetime.now()
                    )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(http_method_names=["GET","PATCH"])
@permission_classes([permissions.IsAuthenticated])
def get_update_business_unit(request:Request, pk:int):
    if request.method == "GET":
        businessUnit = get_object_or_404(BusinessUnit,pk =pk)
        serializer = BusinessUnitSerializer(instance=businessUnit)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == "PATCH":
        businessUnit = get_object_or_404(BusinessUnit, pk = pk)
        serializer = BusinessUnitSerializer(instance=businessUnit, data=request.data)
        if serializer.is_valid():
            serializer.save(
                    updaated_by = request.user,
                    updaated_at = datetime.datetime.now()
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=["GET"])
@permission_classes([permissions.IsAuthenticated])
def list_all_business_units(request:Request):
    businessUnits = BusinessUnit.objects.all()
    serializer = BusinessUnitSerializer(instance=businessUnits, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(http_method_names=["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def delete_business_unit(request:Request, pk:int):
    businessUnit = BusinessUnit.objects.get(pk = pk)
    businessUnit.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(http_method_names=["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def deactivate_business_unit(request:Request, pk:int):
    businessUnit = BusinessUnit.objects.get(pk = pk)
    businessUnit.deleted_at = datetime.datetime.now()
    businessUnit.deleted_by = request.user
    print("**********************************************")
    print("business unit deactivated")
    print("*************************************")
    return Response(status=status.HTTP_200_OK)

@api_view(http_method_names=["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def activate_business_unit(request:Request):
    businessUnit = BusinessUnit.objects.get(pk = pk)
    businessUnit.deleted_at = None
    businessUnit.deleted_by = None
    return Response(status=status.HTTP_200_OK)

@api_view(http_method_names=["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def delete_all_business_units(request:Request):
    businessUnits = BusinessUnit.objects.all()
    for item in businessUnits:
        item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(http_method_names=["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def deactivate_all_business_units(request:Request):
    businessUnits = BusinessUnit.objects.all()
    for item in businessUnits:
        item.deleted_by = request.user
        item.deleted_at = datetime.datetime.now()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(http_method_names=["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def activate_all_business_units(request:Request):
    businessUnits = BusinessUnit.objects.all()
    for item in businessUnits:
        item.deleted_at = None
        item.deleted_by = None
    return Response(status=status.HTTP_200_OK)
