from django.urls import path
from .views import legal_agency_views as v
from .views import business_unit_views as vv

urlpatterns = [
    # legal agency urls
    path(r'legal-agencies', v.LegalAgencyListCreateAPIView.as_view()),
    path(r'legal-agencies/all', v.LegalAgencyListAPIView.as_view()),
    path(r'legal-agencies/<int:pk>', v.get_update_legal_agency),
    path(r'legal-agencies/<int:pk>/deactivate', v.deactivate_legal_agency),
    path(r'legal-agencies/<int:pk>/activate', v.activate_legal_agency),
    path(r'legal-agencies/deactivate/all', v.deactivate_all_legal_agencies),
    path(r'legal-agencies/activate/all', v.activate_all_legal_agencies),
    # business unit urls
    path(r'business-units/', vv.list_create_business_units),
    path(r'business-units/all', vv.list_all_business_units),
    path(r'business-units/<int:pk>', vv.get_update_business_unit),
    path(r'business-units/<int:pk>/deactivate', vv.deactivate_business_unit),
    path(r'business-units/<int:pk>/activate', vv.activate_business_unit),
    path(r'business-units/activate/all', vv.activate_all_business_units),
    path(r'business-units/deactivate/all', vv.deactivate_all_business_units),
    path(r'business-units/<int:pk>/delete', vv.delete_business_unit),
    path(r'business-units/delete/all', vv.delete_all_business_units),
]
