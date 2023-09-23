import datetime

from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from ..models.activity_type import ActivityType
from ..serializers.activity_type_serializer import ActivityTypeSerializer


@api_view(http_method_names=["GET","POST"])
@permission_classes([IsAuthenticated])
def list_create_activity_type(request:Request):
    if request.method == "GET":
        is_deleted = request.query_params.get('is_deleted')
        print(type(is_deleted))
        if is_deleted == '1':
            activityTypes = ActivityType.objects.filter(deleted_at__isnull = False)
            serializer = ActivityTypeSerializer(activityTypes, many = True)
            response = {
                    "message":"deleted activity types",
                    "results": serializer.data
                    }
            return Response(data=response, status=status.HTTP_200_OK)
        if is_deleted == '0':
            activityTypes = ActivityType.objects.filter(deleted_at__isnull = True)
            serializer = ActivityTypeSerializer(activityTypes, many = True)
            response = {
                    "message":"not deleted activity types",
                    "results": serializer.data
                    }
            return Response(data=response, status=status.HTTP_200_OK)
    if request.method == "POST":
        data = request.data
        serializer = ActivityTypeSerializer(data=data)
        if serializer.is_valid():
            serializer.save(
                created_by = request.user,
                created_at = datetime.datetime.now(),
                
            )
            response = {
                "message":"activity type created successfully",
                "results":serializer.data
            }
            return Response(data = response, status=status.HTTP_201_CREATED)
        response = {
            "message":"there was an error creating an activity type",
            "results":serializer.errors
        }
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def list_all_activity_types(request:Request):
    # only list activated activity types
    activityTypes = ActivityType.objects.filter(deleted_at__isnull = True)
    serializer = ActivityTypeSerializer(instance=activityTypes, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(http_method_names=["GET","PATCH"])
@permission_classes([IsAuthenticated])
def get_update_activity_type(request:Request, pk:int):
    if request.method == "GET":
        activityType = ActivityType.objects.get(pk = pk)
        serializer = ActivityTypeSerializer(instance=activityType)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == "PATCH":
        activityType = ActivityType.objects.get(pk = pk)
        serializer = ActivityTypeSerializer(instance=activityType, data=request.data)
        if serializer.is_valid():
            serializer.save(
                    updated_by = request.user,
                    updated_at = datetime.datetime.now()
                    )
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(http_method_names=["DELETE"])
@permission_classes([IsAuthenticated])
def delete_activity_type(request:Request, pk:int):
    activityType = get_object_or_404(ActivityType, pk=pk)
    activityType.delete()
    response = {
        "message":"activity type deleted successfully"
    }
    return Response(data = response, status=status.HTTP_200_OK)



@api_view(http_method_names=["DELETE"])
@permission_classes([IsAuthenticated])
def deactivate_activity_type(request:Request, pk:int):
    activityType = get_object_or_404(ActivityType, pk=pk)
    activityType.deleted_at = datetime.datetime.now()
    activityType.deleted_by = request.user
    activityType.save()
    response = {
        "message":"activity type deactivated successfully"
    }
    return Response(data = response, status=status.HTTP_200_OK)



@api_view(http_method_names=["DELETE"])
@permission_classes([IsAuthenticated])
def activate_activity_type(request:Request, pk:int):
    activityType = get_object_or_404(ActivityType, pk=pk)
    
    activityType.deleted_at = None
    activityType.deleted_by = None
    activityType.save()
    response = {
        "message":"activity type activated successfully"
    }
    return Response(data = response, status=status.HTTP_200_OK)




# delete all activity types
@api_view(http_method_names=["DELETE"])
@permission_classes([IsAuthenticated])
def delete_all_activity_types(request:Request):
    activityTypes = get_list_or_404(ActivityType)
    for item in activityTypes:
        item.delete()
    response = {
        "message":"activity types deleted successfully"
    }
    return Response(data = response, status=status.HTTP_200_OK)



@api_view(http_method_names=["DELETE"])
@permission_classes([IsAuthenticated])
def deactivate_all_activity_types(request:Request):
    activityTypes = get_list_or_404(ActivityType)
    for item in activityTypes:
        item.deleted_at = datetime.datetime.now()
        item.deleted_by = request.user
        item.save()
    response = {
        "message":"activity types deactivated successfully"
    }
    return Response(data = response, status=status.HTTP_200_OK)



@api_view(http_method_names=["DELETE"])
@permission_classes([IsAuthenticated])
def activate_all_activity_types(request:Request):
    activityTypes = get_list_or_404(ActivityType)
    for item in activityTypes:
        
        item.deleted_by = None
        item.deleted_at = None
        item.save()
    response = {
        "message":"activity types activated successfully"
    }
    return Response(data = response, status=status.HTTP_200_OK)
