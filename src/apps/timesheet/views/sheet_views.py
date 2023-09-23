from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..serializers import SheetSerializer
from ..models import Sheet


# create only with created_by field
@api_view(http_method_names=["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_sheet(request: Request):

    data = request.data
    print("***************************************")
    print(data)
    serializer = SheetSerializer(data=data)
    if serializer.is_valid():
        # serializer.save()
        Sheet.objects.create(
            coef=data['coef'],
            user=data['user'],
            activity=data['activity'],
            date=data['date'],
            is_validated=data['is_validated'],
            created_by=request.user,
            created_at=datetime.datetime.now()
        )
        # response = {
        #     "message":"sheet with created by workd hoha",
        #     "results":serializer.data
        # }
        return Response(status=status.HTTP_201_CREATED)
    response = {
        "message": "sheet with created by failed at validation",
        "error": serializer.errors
    }
    return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


# creating and listing sheets
@api_view(http_method_names=["GET", "POST"])
@permission_classes([permissions.IsAuthenticated])
def sheet_list_create(request: Request):
    if request.method == "GET":
        is_validated = request.query_params.get("is_validated")

        if is_validated == '1':
            # list only validated sheets
            # sheets = get_list_or_404(Sheet, is_validated = True)
            sheets1 = Sheet.objects.filter(
                created_by=request.user,
                is_validated=True
            )
            serializer = SheetSerializer(instance=sheets, many=True)
            response = {
                "message": "listing validated sheets",
                "results": serializer.data
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            # list invalidated sheets
            # sheets = get_list_or_404(Sheet, is_validated = False)
            sheets1 = Sheet.objects.filter(
                created_by=request.user,
                is_validated=False
            )
            serializer = SheetSerializer(instance=sheets1, many=True)
            response = {
                "messsage": "listing invalidated sheets",
                "results": serializer.data
            }
            return Response(data=response, status=status.HTTP_200_OK)

    if request.method == "POST":
        data = request.data
        print("*********************************")
        print(data)
        serializer = SheetSerializer(data=data)
        if serializer.is_valid():
            serializer.save(
                created_by=request.user,
                created_at=datetime.datetime.now()
            )
            response = {
                "message": "sheet created successfully",
                "results": serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        response = {
            "message": "failed at creating sheet",
            "results": serializer.errors
        }
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

# show sheet details (only current user && current user's manager can view sheet details)


@api_view(http_method_names=["GET"])
@permission_classes([permissions.IsAuthenticated])
def sheet_details(request: Request, pk: int):
    # sheet = get_object_or_404(Sheet, pk = pk)
    profile = Profile.objects.filter(is_manager=True).select_related('user')
    serializer = SheetSerializer(instance=serializer)
    resposne = {
        "message": "get only current user sheets",
        "results": serializer.data
    }
    return Response(data=serializer.data, status=status.HTTP_200_OK)

# update sheet (only the owner can update his sheet)


@api_view(http_method_names=["PATCH"])
@permission_classes([permissions.IsAuthenticated])
def sheet_update(request: Request, pk: int):
    sheet = get_object_or_404(Sheet, pk=pk)
    data = request.data
    serializer = SheetSerializer(instance=sheet, data=data)
    if serializer.is_valid():
        response = {
            "message": ""
        }

# delete sheet only manager and owner


@api_view(http_method_names=["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def sheet_delete(request: Request, pk: int):
    pass

# deactivating and activating sheets is not obligatory

# validate sheet by the manager
# @api_view(http_method_names=["PATCH"])
# @permission_classes([permissions.IsAuthenticated])
# def validate_sheet(request:Request, pk:int):
#     sheet = Sheet.objects.filter(is_validated = False).get(pk = pk)
#     sheet.
