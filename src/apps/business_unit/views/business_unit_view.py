# from rest_framework import generics, filters
# from rest_framework.permissions import IsAuthenticated
# from ..models.business_unit_model import BusinessUnit
# from ..serializers.business_unit_serializer import BusinessUnitSerializer
# from ..filters import MultiFieldsFilter


# class BusinessUnitListCreateAPIView(generics.ListCreateAPIView):
#     # permission_classes = (IsAuthenticated,)
#     # queryset = BusinessUnit.objects.all()
#     # serializer_class = BusinessUnitSerializer
#     # search_fields = (
#     #     'business_unit_name'
#     # )
#     # filter_backends = [MultiFieldsFilter, filters.OrderingFilter]
#     # ordering_fields = ['business_unit_name']
#     # ordering = ['pk']
#     pass

# class BusinessUnitRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     # permission_classes = (IsAuthenticated,)
#     # queryset = BusinessUnit.objects.all()
#     # serializer_class = BusinessUnitSerializer
#     pass