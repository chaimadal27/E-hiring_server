# python lib
import datetime
# django lib
from rest_framework import generics, filters
from rest_framework import views
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..filters import MultiFieldsFilter
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from apps.core.filters import RelatedOrderingFilter

# custom lib
from ..serializers import CompanySerialiser
from ..models import Company
from apps.core.utils import export_xlsx



"""class CompanyFilter(MultiFieldsFilter):
    def filter_queryset(self, request, queryset, view):
        search_terms = self.get_search_terms(request)
        conditions = self.conditions(search_terms, queryset.model)
        # if search_terms.get('first_name_fr'):
        #     criterion1 = Q(contact__first_name_fr__icontains=search_terms.get('first_name_fr'))
        #     conditions.append(criterion1)
        # if search_terms.get('last_name_fr'):
        #     criterion2 = Q(contact__last_name_fr__icontains=search_terms.get('last_name_fr'))
        #     conditions.append(criterion2)
        # if search_terms.get('telephone'):
        #     criterion3 = Q(contact__telephone__icontains=search_terms.get('telephone'))
        #     conditions.append(criterion3)
        return queryset.filter(*conditions)"""


class CompanyCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CompanySerialiser
    permission_classes = [IsAuthenticated]
    queryset = Company.objects.all()
    search_fields = (
        'name_fr',
        'name_ar',
        'address_fr',
        'address_ar',
        'staff',
        'activity',
        'telephone',
        'email',
        'web_site'
    )
    filter_backends = [MultiFieldsFilter, filters.OrderingFilter]
    ordering_fields = ['name_fr']
    ordering = ['pk']

    # def filter_queryset(self, queryset):
    #     qs = super().filter_queryset(queryset)
    #     filter_kwargs = {}
    #     is_active = self.request.query_params.get('is_active', None)
    #     try:
    #         is_deleted = int(is_active)
    #         filter_kwargs.update(deleted_at__isnull=is_deleted)
    #     except ValueError:
    #         pass
    #     return qs.filter(**filter_kwargs)

class CompanyRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = CompanySerialiser
    permission_classes = [IsAuthenticated]
    queryset = Company.objects.filter(
        deleted_at__isnull=True,
    )


class AllCompaniesListAPIView(generics.ListAPIView):
    queryset = Company.objects.filter(
        deleted_at__isnull=True,
    )
    permission_classes = [IsAuthenticated]
    serializer_class = CompanySerialiser
    pagination_class = None


class CompanyDeactivateAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CompanySerialiser
    queryset = Company.objects.filter(
        deleted_at__isnull=True,
    )

    def perform_destroy(self, instance):
        instance.deleted_by = self.request.user
        instance.deleted_at = datetime.datetime.now()
        instance.save()
        contact_set = instance.contact_set.all().update(deleted_by=self.request.user, deleted_at=datetime.datetime.now())


class CompanyActivateAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CompanySerialiser
    queryset = Company.objects.filter(
        deleted_at__isnull=False,
    )

    def perform_destroy(self, instance):
        instance.deleted_by = None
        instance.deleted_at = None
        instance.save()
        contact_set = instance.contact_set.all().update(deleted_by=None,deleted_at=None)


class ExportCompany(views.APIView):
    def get(self, request):
        ids_param = request.query_params.getlist('ids[]')
        companies = Company.get_companies(ids_param)
        data = export_xlsx(queryset=companies[0],
                          fields=companies[1],
                          titles=companies[2],
                          file_name='list_Company',
                          sheet_name='Company')
        return data

class  AllCompaniesNamesList(generics.ListAPIView):
    queryset = Company.objects.filter(
        deleted_at__isnull=True,
    )
    permission_classes = [IsAuthenticated]
    serializer_class = CompanySerialiser
    pagination_class = None

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.filter()

