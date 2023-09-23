# django lib
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
# custom lib
from ..serializers import ContactSerializer
from ..models import Contact,Company


class ContactCreateAPIView(ListCreateAPIView):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    queryset = Contact.objects.filter(
        deleted_at__isnull=True,
    )


class ContactRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    queryset = Contact.objects.filter(
        deleted_at__isnull=True,
    )
class  AllContactsByCompanyList(generics.ListAPIView):
    queryset = Contact.objects.filter(
        deleted_at__isnull=True,
    )
    permission_classes = [IsAuthenticated]
    serializer_class = ContactSerializer
    pagination_class = None

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        company_id = self.request.query_params.get('id')
        if company_id:
            company = Company.objects.get(id=company_id)
            return queryset.filter(company=company)
        else:
            return queryset