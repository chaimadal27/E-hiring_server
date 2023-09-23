# python lib
import datetime
# django lib
from rest_framework import generics, filters
from rest_framework import views
from rest_framework.permissions import IsAuthenticated


# custom lib
from ..serializers import JobCategorySerialiser
from ..models import JobCategory
from apps.core.utils import export_xlsx



class JobCategoryCreateAPIView(generics.ListCreateAPIView):
    serializer_class = JobCategorySerialiser
    permission_classes = [IsAuthenticated]
    queryset = JobCategory.objects.all()
    search_fields = (
        'name_fr',
        'name_ar',
    )

    ordering_fields = ['name_fr']
    ordering = ['pk']


class JobCategoryRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = JobCategorySerialiser
    permission_classes = [IsAuthenticated]
    queryset = JobCategory.objects.filter(
        deleted_at__isnull=True,
    )


class AllJobCategoriesListAPIView(generics.ListAPIView):
    queryset = JobCategory.objects.filter(
        deleted_at__isnull=True,
    )
    permission_classes = [IsAuthenticated]
    serializer_class = JobCategorySerialiser
    pagination_class = None


class JobCategoryDeactivateAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = JobCategorySerialiser
    queryset = JobCategory.objects.filter(
        deleted_at__isnull=True,
    )

    def perform_destroy(self, instance):
        instance.deleted_by = self.request.user
        instance.deleted_at = datetime.datetime.now()
        instance.save()
        job_set = instance.job_set.all().update(deleted_by=self.request.user, deleted_at=datetime.datetime.now())


class JobCategoryActivateAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = JobCategorySerialiser
    queryset = JobCategory.objects.filter(
        deleted_at__isnull=False,
    )

    def perform_destroy(self, instance):
        instance.deleted_by = None
        instance.deleted_at = None
        instance.save()
        job_set = instance.job_set.all().update(deleted_by=None,
                                                        deleted_at=None)


class ExportJobCategory(views.APIView):
    def get(self, request):
        ids_param = request.query_params.getlist('ids[]')
        categories = JobCategory.get_categories(ids_param)
        data = export_xlsx(queryset=categories[0],
                          fields=categories[1],
                          titles=categories[2],
                          file_name='list_JobCategory',
                          sheet_name='JobCategory')
        return data
