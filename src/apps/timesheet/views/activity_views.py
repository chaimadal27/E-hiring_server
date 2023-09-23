import datetime
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request


from ..models.activity import Activity
from ..serializers.activity_serializer import ActivitySerializer

# listing and creating activities


@api_view(http_method_names=["GET", "POST"])
@permission_classes([IsAuthenticated])
def list_create_activity(request: Request):
    if request.method == "GET":
        is_deleted = request.query_params.get('is_deleted')
        if is_deleted == '1':
            activities = Activity.objects.filter(deleted_at__isnull=False)
            serializer = ActivitySerializer(instance=activities, many=True)
            response = {
                "message": "activities that are deactivated",
                "results": serializer.data
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            activities = Activity.objects.filter(deleted_at__isnull=True)
            serializer = ActivitySerializer(instance=activities, many=True)
            response = {
                "message": "activities that are not deactivated",
                "results": serializer.data
            }
            return Response(data=response, status=status.HTTP_200_OK)

    if request.method == "POST":
        data = request.data
        serializer = ActivitySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def get_update_activity(request: Request, pk: int):
    if request.method == "GET":
        activity = get_object_or_404(Activity, pk=pk)
        serializer = ActivitySerializer(instance=activity)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == "PATCH":
        activity = get_object_or_404(Activity, pk=pk)
        serializer = ActivitySerializer(instance=activity, data=request.data)
        if serializer.is_valid():
            serializer.save(
                updated_by=request.user,
                updated_at=datetime.datetime.now()
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_200_OK)

# delete activity


@api_view(http_method_names=["DELETE"])
@permission_classes([IsAuthenticated])
def delete_activity(request: Request, pk: int):
    activity = get_object_or_404(Activity, pk=pk)
    activity.delete()
    response = {
        "message": "activity deleted successfully"
    }
    return Response(data=response, status=status.HTTP_200_OK)


# delete all activities
@api_view(http_method_names=["DELETE"])
@permission_classes([IsAuthenticated])
def delete_all_activities(request: Request):
    activities = get_list_or_404(Activity)
    for item in activities:
        item.delete()
    response = {
        "message": "all activities deleted successfully"
    }
    return Response(data=response, status=status.HTTP_200_OK)


# deactivate activity
@api_view(http_method_names=["DELETE"])
@permission_classes([IsAuthenticated])
def deactivate_activity(request: Request, pk: int):
    activity = get_object_or_404(Activity, pk=pk)
    activity.is_deleted = True
    activity.deleted_by = request.user
    activity.deleted_at = datetime.datetime.now()
    activity.save()
    response = {
        "message": "activity deactivated successfully"
    }
    return Response(data=response, status=status.HTTP_200_OK)


# deactivate all activities
@api_view(http_method_names=["DELETE"])
@permission_classes([IsAuthenticated])
def deactivate_all_activities(request: Request):
    activities = get_list_or_404(Activity)
    for item in activities:
        item.is_deleted = True
        item.deleted_by = request.user
        item.deleted_at = datetime.datetime.now()
        item.save()
    response = {
        "message": "all activities are deactivated"
    }
    return Response(data=response, status=status.HTTP_200_OK)


# activate activity
@api_view(http_method_names=["DELETE"])
@permission_classes([IsAuthenticated])
def activate_activity(request: Request, pk: int):
    activity = get_object_or_404(Activity, pk=pk)
    activity.is_deleted = False
    activity.deleted_at = None
    activity.deleted_by = None
    activity.save()
    response = {
        "message": "activity activated successfully"
    }
    return Response(data=response, status=status.HTTP_200_OK)


# activate all activities
@api_view(http_method_names=["DELETE"])
@permission_classes([IsAuthenticated])
def activate_all_activity(request: Request):
    activities = get_list_or_404(Activity)
    for item in activities:
        item.is_deleted = False
        item.deleted_at = None
        item.deleted_by = None
        item.save()
    response = {
        "message": "all activities are activated"
    }
    return Response(data=response, status=status.HTTP_200_OK)

# export activities


@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def export_activities(request: Request):
    pass
