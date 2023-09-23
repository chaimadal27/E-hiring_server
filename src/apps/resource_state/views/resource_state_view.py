import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import generics


from ..models.resource_state_model import ResourceState
from ..serializers.resource_state_serializer import ResourceStateSerializer


# creating and listing resource states
@api_view(http_method_names=["GET","POST"])
@permission_classes([IsAuthenticated])
def list_create_resource_state(request:Request):
    if request.method == "GET":
        is_deleted = request.query_params.get('is_deleted')
        if is_deleted == '1':
            reousrceState = ResourceState.objects.filter(
                    deleted_at__isnull = False
                    )
            serializer = ResourceStateSerializer(instance=resourceStates, many = True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            resourceStates = ResourceState.objects.filter(
                    deleted_at__isnull = True
                    )
            serializer = ResourceStateSerializer(instance=resourceStates, many = True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == "POST":
        data = request.data
        serializer = ResourceStateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# get update reousrce state
@api_view(http_method_names=["GET","PATCH"])
@permission_classes([IsAuthenticated])
def get_update_resource_state(request:Request, pk:int):
    if request.method == "GET":
        resourceState = ResourceState.objects.get(pk = pk)
        serializer = ResourceStateSerializer(instance=resourceState)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == "PATCH":
        resourceState = ResourceState.objects.get(pk = pk)
        serializer = ResourceStateSerializer(instance=resourceState, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# delete resource state
@api_view(http_method_names=["DELETE"])
@permission_classes([IsAuthenticated])
def delete_resource_state(request:Request, pk:int):
    resourceState = get_object_or_404(ResourceState, pk = pk)
    resourceState.delete()
    response = {
        "message":"resource state deleted sucessfully"
    }
    return Response(data=response, status=status.HTTP_200_OK)
# delete all resource states
@api_view(http_method_names=["DELETE"])
@permission_classes([IsAuthenticated])
def delete_all_resource_states(request:Request):
    resourceStates = ResourceState.objects.all().filter(
        deleted_at__isnull = True
    )
    for item in resourceStates:
        item.delete()
    
    response = {
        "message":"all resource state deleted successfully"
    }
    return Response(data=response, status=state.HTTP_200_OK)

# deactivate resource state
@api_view(http_method_names=["DELETE"])
@permission_classes([IsAuthenticated])
def deactivate_resource_state(request:Request, pk:int):
    resourceState = get_object_or_404(ResourceState, pk = pk)
    resourceState.deleted_at = datetime.datetime.now()
    resourceState.deleted_by = request.user
    resourceState.save()
    response = {
        "message":"resource state deactivated successfully",
    }
    return Response(data=response, status=status.HTTP_200_OK)

# activate reousrce state
@api_view(http_method_names=["DELETE"])
@permission_classes([IsAuthenticated])
def activate_resource_state(request:Request, pk:int):
    resourceState = get_object_or_404(ResourceState, pk = pk)
    resourceState.deleted_at = None
    resourceState.deleted_by = None
    resourceState.save()
    response = {
        "message":"resource state activated succesfully"
    }
    return Response(data=response, status=status.HTTP_200_OK)

# deactivate all resource states
@api_view(http_method_names=["DELETE"])
@permission_classes([IsAuthenticated])
def deactivate_all_resource_states(request:Request):
    resourceStates = ResourceState.objects.all().filter(
        deleted_at__isnull = True
    )
    for item in resourceStates:
        item.deleted_at = datetime.datetime.now()
        item.deleted_by = request.user
        item.save()
    response = {
        "message":"all resource states are deactivated"
    }
    return Response(data=response, status=status.HTTP_200_OK)
# activate all resource states
@api_view(http_method_names=["DELETE"])
@permission_classes([IsAuthenticated])
def activate_all_resource_states(request:Request):
    resourceStates = ResourceState.objects.all().filter(
        deleted_at__isnull = False
    )
    for item in resourceStates:
        item.deleted_at = None
        item.deleted_by = None
        item.save()
    response = {
        "message":"all resources are activated"
    }
    return Response(data=response, status=status.HTTP_200_OK)
