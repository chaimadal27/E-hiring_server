# from rest_framework import serializers
# from ..models.business_unit_model import BusinessUnit
# from ...legal_agency.models.legal_agency_model import LegalAgency
# from ...user_managment.models.profile import Profile
# class BusinessUnitSerializer(serializers.ModelSerializer):
#     # legal_agency = serializers.PrimaryKeyRelatedField(
#     #     read_only = False,
#     #     queryset = LegalAgency.objects.all()
#     # )
#     # business_unit_manager = serializers.PrimaryKeyRelatedField(
#     #     read_only = False,
#     #     # insures that only the user with the flag is_manager = True can be a business unit manager
#     #     queryset = Profile.objects.select_related('user').filter(
#     #         is_manager=True
#     #     )
#     # )
#     # class Meta:
#     #     model = BusinessUnit
#     #     fields = ('id', 'business_unit_name', 'legal_agency', 'business_unit_manager')
#     pass