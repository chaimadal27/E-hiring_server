# Offers views
from .offer_views import OfferCreateAPIView,\
    OfferDeactivateAPIView,OfferActivateAPIView,\
    OfferRetrieveUpdateAPIView,AllOffersListAPIView,\
    AllRecruitersByOfferList, AllOffersNamesList,ValidOfferView,OfferCloseAPIView,ExportOffer
# Kanban views
from .kanban_views import KanbanCreateAPIView,KanbanRetrieveUpdateAPIView,\
    AllKanbanCandidatesListAPIView,ChangeKanbanStageAPIView,DeleteKanabanAPIView
#Appointment views
from .appointment_views import AppointmentCreateAPIView,AppointmentsListByOfferAPIView,\
    AppointmentRetrieveUpdateAPIView,AppointmentsOfferListAPIView,MyAppointmentsListAPIView,MyRecentAppointmentsListAPIView,AppointmentDeactivateAPIView