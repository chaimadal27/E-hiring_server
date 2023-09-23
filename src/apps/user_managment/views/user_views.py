import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, status
# trying api_view, permission_classes
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.core.filters import RelatedOrderingFilter

from ..models import Profile
from ..serializers import ProfileSerializer, SimpleUserSerializer

User = get_user_model()


class UserListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    search_fields = (
        'phone',
        'second_phone',
        'user__first_name',
        'user__last_name',
        'user__email',

    )
    filter_backends = [filters.SearchFilter, RelatedOrderingFilter]
    ordering_fields = '__all__'
    ordering = ['pk']

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        filter_kwargs = {'user__is_superuser': False}
        is_active = self.request.query_params.get('is_active', None)
        is_deleted = self.request.query_params.get('is_deleted', None)
        if is_active:
            try:
                is_active = int(is_active)
                filter_kwargs.update(deleted_at__isnull=is_active)
            except ValueError:
                pass

        if is_deleted:
            try:
                is_deleted = bool(int(is_deleted))
                filter_kwargs.update(is_deleted=is_deleted)
            except ValueError:
                pass
        return qs.filter(**filter_kwargs)


class DisplayAdminUsers(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.filter(
        user__is_superuser=True
    )


class ALLCPSListAPIView(generics.ListAPIView):
    """
       List of ALL users cps.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = SimpleUserSerializer
    queryset = User.objects.filter(is_active=True)
    pagination_class = None

    def get_queryset(self):
        cp_group = Group.objects.get(name=settings.CP_GROUP_NAME)
        return cp_group.user_set.all()


class ALLUserListAPIView(generics.ListAPIView):
    """
       List of ALL users.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = SimpleUserSerializer
    # queryset = User.objects.filter(is_active=True,)*$
    queryset = User.objects.all()
    pagination_class = None


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    # queryset = Profile.objects.filter(deleted_at__isnull=True, user__is_superuser=False)
    queryset = Profile.objects.filter(deleted_at__isnull=True)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data
        user = data.get('user', None)
        import pprint
        pp = pprint.PrettyPrinter(depth=6)
        pp.pprint('**********************************')
        pp.pprint(data)
        pp.pprint(instance.user.email)
        pp.pprint('**********************************')
        if user and user.get('email', None) == instance.user.email:
            user.pop('email', None)

        import pprint
        pp = pprint.PrettyPrinter(depth=6)
        pp.pprint('**********************************')
        pp.pprint(data)
        pp.pprint('**********************************')
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


# class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = ProfileSerializer
#     queryset = Profile.objects.filter(deleted_at__isnull=True)
#
#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         data = request.data
#         user = data.get('user', None)
#         import pprint
#         pp = pprint.PrettyPrinter(depth=6)
#         pp.pprint('**********************************')
#         pp.pprint(data)
#         pp.pprint(instance.user.email)
#         pp.pprint('**********************************')
#         if user and user.get('email', None) == instance.user.email:
#             user.pop('email', None)
#
#         import pprint
#         pp = pprint.PrettyPrinter(depth=6)
#         pp.pprint('**********************************')
#         pp.pprint(data)
#         pp.pprint('**********************************')
#         serializer = self.get_serializer(instance, data=data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#
#         if getattr(instance, '_prefetched_objects_cache', None):
#             # If 'prefetch_related' has been applied to a queryset, we need to
#             # forcibly invalidate the prefetch cache on the instance.
#             instance._prefetched_objects_cache = {}
#
#         return Response(serializer.data)


class UserDeactivateAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except:
            raise Http404

    def delete(self, request, pk):
        profile = self.get_object(pk)
        profile.user.is_active = True
        profile.deleted_at = datetime.datetime.now()
        profile.deleted_by = request.user
        profile.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserActivateAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    queryset = Profile.objects.filter(
        deleted_at__isnull=False,
        user__is_superuser=False,
        is_deleted=False
    )

    def perform_destroy(self, instance):
        instance.deleted_by = None
        instance.deleted_at = None
        instance.user.is_active = True
        instance.user.save()
        instance.save()


class UserDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    queryset = Profile.objects.filter(
        deleted_at__isnull=False,
        user__is_superuser=False,
        is_deleted=False
    )

    def perform_destroy(self, instance):
        instance.deleted_by = self.request.user
        instance.deleted_at = datetime.datetime.now()
        instance.user.is_active = False
        instance.user.save()
        instance.is_deleted = True
        instance.save()


class UserUnDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    queryset = Profile.objects.filter(
        deleted_at__isnull=False,
        user__is_superuser=False,
        is_deleted=True
    )

    def perform_destroy(self, instance):
        instance.deleted_by = None
        instance.deleted_at = None
        instance.user.is_active = True
        instance.user.save()
        instance.is_deleted = False
        instance.save()


class ManagerAPIView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


# class UpdateUserAPIView(generics.UpdateAPIView):
#     serializer_class = ProfileSerializer

#     def get_object(self, pk):
#         try:
#             return Profile.objects.get(pk = pk)
#         except:
#             raise Http404


#     def patch(self, request, pk, *args, **kwargs):
#         profile = self.get_object(pk)
#         print(profile.id)
#         print("*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/")
#         data = request.data
#         print(data)
#         serializer = self.get_serializer(profile, data=request.data)
#         print("*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/")
#         if serializer.is_valid() is False:

#             print(serializer.errors)

#             return Response(status=status.HTTP_204_NO_CONTENT)
#         serializer.save()
#         # print(serializer.data)
#         return Response(serializer.data,status=status.HTTP_201_CREATED)

@api_view(http_method_names=["PATCH"])
@permission_classes([IsAuthenticated])
def update_user(request: Request, pk: int):
    profile = get_object_or_404(Profile, pk=pk)
    print("-----------------------")
    data = request.data
    print("-----------------------")
    serializer = ProfileSerializer(instance=profile, data=data)
    if serializer.is_valid():
        serializer.save(
            updated_by=request.user,
            updated_at=datetime.datetime.now()
        )
        response = {
            "message": "user updated successfully",
            "results": serializer.data
        }
        return Response(data=response, status=status.HTTP_200_OK)
        response = {
            "message": "failed at validation",
            "results": serializer.errors
        }
    return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
