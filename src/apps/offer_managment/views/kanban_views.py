# python lib
import datetime
# django lib
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework import views
from rest_framework.response import Response
# custom lib
from ..serializers import KanbanSerializer
from ..models import Kanban,Offer
from apps.candidate_managment.models import Candidate
from apps.candidate_managment.serializers import CandidateSerializer

class KanbanCreateAPIView(generics.ListCreateAPIView):
    serializer_class = KanbanSerializer
    permission_classes = [IsAuthenticated]
    queryset = Kanban.objects.all()
    ordering = ['pk']


class KanbanRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = KanbanSerializer
    permission_classes = [IsAuthenticated]
    queryset = Kanban.objects.filter(
        deleted_at__isnull=True,
    )


class AllKanbanCandidatesListAPIView(generics.ListAPIView):
    queryset = Kanban.objects.filter(
        deleted_at__isnull=True,
    )
    permission_classes = [IsAuthenticated]
    serializer_class = KanbanSerializer
    pagination_class = None

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        offer_id = self.request.query_params.get('offer')
        # candidate_ids=[instance.candidate.id for instance in Kanban.objects.filter(offer=offer_id)]
        # print(candidate_ids)
        # return queryset.filter(id__in=candidate_ids)
        return queryset.filter(offer=offer_id)

class  ChangeKanbanStageAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        kanban_id = self.request.query_params.get('id')
        destination=self.request.query_params.get('stage')
        print(destination)
        Kanban.objects.filter(id=kanban_id).update(stage_candidate=destination)
        return Response(True)

class  DeleteKanabanAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        kanban_id = self.request.query_params.get('id')
        kanban=Kanban.objects.get(id=kanban_id)
        kanban.delete()
        return Response(True)