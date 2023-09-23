# python lib
import datetime
# django lib
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework import views
from rest_framework.response import Response
from django.conf import settings



# custom lib
from ..serializers import OfferSerializer,OfferListSerializer
from ..models import Offer
from apps.core.utils import export_xlsx
from django.contrib.auth import get_user_model
from apps.user_managment.serializers import SimpleUserSerializer
from apps.referentiel_managment.filters import MultiFieldsFilter

User = get_user_model()



class OfferCreateAPIView(generics.ListCreateAPIView):
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]
    queryset = Offer.objects.all()
    search_fields = (
        'title',
        'country',
    )
    filter_backends = [MultiFieldsFilter, filters.OrderingFilter]
    ordering_fields = ['title']
    ordering = ['pk']


class OfferRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]
    queryset = Offer.objects.filter(
        deleted_at__isnull=True,
    )


class AllOffersListAPIView(generics.ListAPIView):
    queryset = Offer.objects.filter(
        deleted_at__isnull=True,
    )
    permission_classes = [IsAuthenticated]
    serializer_class = OfferSerializer
    pagination_class = None


class OfferDeactivateAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OfferSerializer
    queryset = Offer.objects.filter(
        deleted_at__isnull=True,
        # is_active=True
    )

    def perform_destroy(self, instance):
        instance.deleted_by = self.request.user
        instance.deleted_at = datetime.datetime.now()
        # instance.is_active=False
        instance.save()


class OfferActivateAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OfferSerializer
    queryset = Offer.objects.filter(
        deleted_at__isnull=False,
        # is_active=False
    )

    def perform_destroy(self, instance):
        instance.deleted_by = None
        instance.deleted_at = None
        # instance.is_active=True
        instance.save()

class ValidOfferView(generics.RetrieveAPIView):
    queryset = Offer.objects.filter(
        deleted_at__isnull=True,
    )
    serializer_class = OfferSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_valid = True
        instance.status = settings.IN_PROCESSING_STATUS
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class OfferCloseAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OfferSerializer
    queryset = Offer.objects.filter(
        deleted_at__isnull=True,
        # is_active=True
    )

    def perform_destroy(self, instance):
        instance.status=settings.CLOSE_STATUS
        instance.save()

class AllOffersNamesList(generics.ListAPIView):
    queryset = Offer.objects.filter(
        deleted_at__isnull=True,
    )
    permission_classes = [IsAuthenticated]
    serializer_class = OfferListSerializer
    pagination_class = None

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.filter(is_valid=True)

class  AllRecruitersByOfferList(views.APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SimpleUserSerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        offer_id = self.request.query_params.get('id')
        offer = Offer.objects.get(id=offer_id)
        return Response (offer.recruiter.all().values())


class ExportOffer(views.APIView):
    def get(self, request):
        ids_param = request.query_params.getlist('ids[]')
        schools = Offer.get_schools(ids_param)
        data = export_xlsx(queryset=schools[0],
                           fields=schools[1],
                           titles=schools[2],
                           file_name='list_Offer',
                           sheet_name='Offer')
        return data