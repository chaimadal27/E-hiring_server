from django.urls import path
from .views.global_settings_views import GlobalSettingsListCreateAPIView, GlobalSettingsRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('global-settings/', GlobalSettingsListCreateAPIView.as_view()),
    path('global-settings/<int:pk>/', GlobalSettingsRetrieveUpdateDestroyAPIView.as_view()),
]