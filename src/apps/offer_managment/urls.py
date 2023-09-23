from django.urls import path

from . import views

urlpatterns = [
    # offers urls
    path(r'offers', views.OfferCreateAPIView.as_view()),
    path(r'offers/<int:pk>', views.OfferRetrieveUpdateAPIView.as_view()),
    path(r'offers/<int:pk>/activate', views.OfferActivateAPIView.as_view()),
    path(r'offers/<int:pk>/deactivate', views.OfferDeactivateAPIView.as_view()),
    path(r'offers/<int:pk>/validate', views.ValidOfferView.as_view()),
    path(r'offers/<int:pk>/close', views.OfferCloseAPIView.as_view()),
    path(r'offers/all', views.AllOffersListAPIView.as_view()),
    path(r'offers/list', views.AllOffersNamesList.as_view()),
    path(r'offers/export', views.ExportOffer.as_view()),
    path(r'offers/recruiters/list', views.AllRecruitersByOfferList.as_view()),

    # kanban urls
    path(r'kanban', views.KanbanCreateAPIView.as_view()),
    path(r'kanban/<int:pk>', views.KanbanRetrieveUpdateAPIView.as_view()),
    path(r'kanban/candidates', views.AllKanbanCandidatesListAPIView.as_view()),
    path(r'kanban/change_stage', views.ChangeKanbanStageAPIView.as_view()),
    path(r'kanban/delete', views.DeleteKanabanAPIView.as_view()),

    # Appointment routes
    path(r'offers/<int:pk>/appointments', views.AppointmentsOfferListAPIView.as_view()),
    path(r'appointments', views.AppointmentCreateAPIView.as_view()),
    path(r'myself/appointments', views.MyAppointmentsListAPIView.as_view()),
    path(r'myself/appointments/<int:pk>', views.AppointmentRetrieveUpdateAPIView.as_view()),
    path(r'myself/appointments/recent', views.MyRecentAppointmentsListAPIView.as_view()),
    path(r'offers/<int:pk>/appointments', views.AppointmentsListByOfferAPIView.as_view()),
    path(r'appointments/<int:pk>', views.AppointmentRetrieveUpdateAPIView.as_view()),
    path(r'appointment/<int:pk>/deactivate', views.AppointmentDeactivateAPIView.as_view()),
]