# python lib
import datetime
# django lib
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework import views

# custom lib
from ..serializers import SchoolSerialiser
from ..models import School
from apps.core.utils import export_xlsx
from ..filters import MultiFieldsFilter



class SchoolCreateAPIView(generics.ListCreateAPIView):
    serializer_class = SchoolSerialiser
    permission_classes = [IsAuthenticated]
    queryset = School.objects.all()
    search_fields = (
        'short_name_fr',
        'long_name_fr',
        'short_name_ar',
        'long_name_ar',
        'web_site',
        'type',
        'country',
    )
    filter_backends = [MultiFieldsFilter, filters.OrderingFilter]
    ordering_fields = ['short_name_fr']
    ordering = ['pk']

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        filter_kwargs = {}
        is_active = self.request.query_params.get('is_active', None)
        try:
            is_active = int(is_active)
            filter_kwargs.update(deleted_at__isnull=is_active)
        except ValueError:
            pass
        return qs.filter(**filter_kwargs)


class SchoolRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = SchoolSerialiser
    permission_classes = [IsAuthenticated]
    queryset = School.objects.filter(
        deleted_at__isnull=True,
    )


class AllSchoolsListAPIView(generics.ListAPIView):
    queryset = School.objects.filter(
        deleted_at__isnull=True,
    )
    permission_classes = [IsAuthenticated]
    serializer_class = SchoolSerialiser
    pagination_class = None


class SchoolDeactivateAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SchoolSerialiser
    queryset = School.objects.filter(
        deleted_at__isnull=True,
        # is_active=True
    )

    def perform_destroy(self, instance):
        instance.deleted_by = self.request.user
        instance.deleted_at = datetime.datetime.now()
        # instance.is_active=False
        instance.save()



class SchoolActivateAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SchoolSerialiser
    queryset = School.objects.filter(
        deleted_at__isnull=False,
        # is_active=False
    )

    def perform_destroy(self, instance):
        instance.deleted_by = None
        instance.deleted_at = None
        # instance.is_active=True
        instance.save()

class  AllSchoolsNamesList(generics.ListAPIView):
    queryset = School.objects.filter(
        deleted_at__isnull=True,
    )
    permission_classes = [IsAuthenticated]
    serializer_class = SchoolSerialiser
    pagination_class = None

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.values('id','short_name_fr','long_name_fr')

class ExportSchool(views.APIView):
    def get(self, request):
        ids_param = request.query_params.getlist('ids[]')
        schools = School.get_schools(ids_param)
        data = export_xlsx(queryset=schools[0],
                          fields=schools[1],
                          titles=schools[2],
                          file_name='list_School',
                          sheet_name='School')
        return data