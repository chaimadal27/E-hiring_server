from django.urls import re_path, include

urlpatterns = [
    re_path(r'^', include('apps.jwt_authentication.urls')),
    re_path(r'^', include('apps.user_managment.urls')),
    re_path(r'^', include('apps.referentiel_managment.urls')),
    re_path(r'^', include('apps.lists_managment.urls')),
    re_path(r'^', include('apps.candidate_managment.urls')),
    re_path(r'^', include('apps.offer_managment.urls')),
    # timetracking urls <3 <3 :)
    re_path(r'^', include('apps.legal_agency.urls')),
    re_path(r'^', include('apps.timesheet.urls')),
    re_path(r'^', include('apps.resource_state.urls')),
    re_path(r'^', include('apps.global_settings.urls')),
]
