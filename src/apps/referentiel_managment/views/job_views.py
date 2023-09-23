# django lib
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, filters
from rest_framework.response import Response
from django.conf import settings
# custom lib
from ..serializers import JobSerializer
from ..models import Job,JobCategory


class JobCreateAPIView(ListCreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
    queryset = Job.objects.filter(
        deleted_at__isnull=True,
    )


class JobRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
    queryset = Job.objects.filter(
        deleted_at__isnull=True,
    )
    
class  AllJobsByCategoryList(generics.ListAPIView):
    queryset = Job.objects.filter(
        deleted_at__isnull=True,
    )
    permission_classes = [IsAuthenticated]
    serializer_class = JobSerializer
    pagination_class = None

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        name = self.request.query_params.get('name_fr')
        category = JobCategory.objects.get(name_fr=name)
        return queryset.filter(category=category)

class JobValidateAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = JobSerializer
    queryset = Job.objects.filter(
        deleted_at__isnull=False,)

    def perform_destroy(self, instance):
        instance.deleted_by = None
        instance.deleted_at = None
        instance.save()


class ValidJobView(generics.RetrieveAPIView):
    queryset = Job.objects.filter(
        deleted_at__isnull=True,
    )
    serializer_class = JobSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = settings.VALID_STATUS
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class RejectJobView(generics.RetrieveAPIView):
    queryset = Job.objects.filter(
        deleted_at__isnull=True,
    )
    serializer_class = JobSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = settings.REJECT_STATUS
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)