# python lib
import datetime
# django lib
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, filters, status,serializers
from rest_framework.permissions import IsAuthenticated
from ..filters import MultiFieldsFilter
from apps.core.generics import ActionViewBase
from apps.user_managment.serializers import SimpleUserSerializer
from apps.jwt_authentication.send_mail import send_mail_on_share_candidate_cv
from apps.core.models import User
import os
import base64
from django.conf import settings
from django.db.models import Q

# custom lib
from ..serializers import CandidateSerializer,ShareCVSerializer
from ..models import Candidate,Document

class CandidateFilter(MultiFieldsFilter):
    def filter_queryset(self, request, queryset, view):
        search_terms = self.get_search_terms(request)
        conditions = self.conditions(search_terms, queryset.model)
        # if search_terms.get('email'):
        #     criterion1 = Q(candidate__first_name_fr__icontains=search_terms.get('email'))
        #     conditions.append(criterion1)
        # if search_terms.get('last_name_fr'):
        #     criterion2 = Q(candidate__last_name_fr__icontains=search_terms.get('last_name_fr'))
        #     conditions.append(criterion2)
        # if search_terms.get('first_name_fr'):
        #     criterion3 = Q(candidate__telephone__icontains=search_terms.get('first_name_fr'))
        #     conditions.append(criterion3)
        return queryset.filter(*conditions)

class CandidateCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticated]
    queryset = Candidate.objects.all()
    search_fields = (
        'first_name_fr',
        'last_name_ar',
        'email',
    )
    filter_backends = [MultiFieldsFilter]
    ordering_fields = ['first_name_fr']
    ordering = ['pk']


class CandidateRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticated]
    queryset = Candidate.objects.filter(
        deleted_at__isnull=True,
    )


class AllCandidatesListAPIView(generics.ListAPIView):
    queryset = Candidate.objects.filter(
        deleted_at__isnull=True,
    )
    permission_classes = [IsAuthenticated]
    serializer_class = CandidateSerializer
    pagination_class = None


class CandidateDeactivateAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CandidateSerializer
    queryset = Candidate.objects.filter(
        deleted_at__isnull=True,
    )

    def perform_destroy(self, instance):
        instance.deleted_by = self.request.user
        instance.deleted_at = datetime.datetime.now()
        instance.save()
        languagedetail_set = instance.languagedetail_set.all().update(deleted_by=self.request.user, deleted_at=datetime.datetime.now())


class CandidateActivateAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CandidateSerializer
    queryset = Candidate.objects.filter(
        deleted_at__isnull=False,
    )

    def perform_destroy(self, instance):
        instance.deleted_by = None
        instance.deleted_at = None
        instance.save()
        languagedetail_set = instance.languagedetail_set.all().update(deleted_by=None,deleted_at=None)

class GetCVAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticated]
    queryset = Candidate.objects.filter(
        deleted_at__isnull=True,
    )
    # def get(self,queryset, request, *args, **kwargs):
    #     documents=queryset.get('document_set').values().first()
    #     print(documents,'ooooooooooooooooooooooooooooooooo')
    #     cv = queryset.objects.filter(candidate=id, type=1).values().first()
    #     if cv :
    #         return Response(cv.get('file'))
    #     else :
    #         return Response("example.pdf")

class  ValidateEmailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        email = self.request.query_params.get('email')
        return Response(not Candidate.objects.filter(email=email).exists())

class ShareCandidateCVAPIView(ActionViewBase):
    permission_classes = [IsAuthenticated]
    serializer_class = ShareCVSerializer

    def post(self, request, *args, **kwargs):
        user=request.user
        id = self.request.query_params.get('id')
        serializer = self.get_serializer(data=request.data, context={'request': request, 'kwargs': kwargs})
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data:
            users_list=list(serializer.validated_data.items())[0][1]
            users=[User.objects.get(id=id) for id in users_list]
            candidate=Candidate.objects.get(id=id)
            files=Document.objects.filter(candidate=candidate).filter(type=1).first()
            file=files.file
            file_name=os.path.basename(file.name)
            with open(file.path, 'rb') as f:
                data = f.read()
                f.close()
            encoded_file = base64.b64encode(data).decode()
            print(encoded_file, '*********************************')

            # with file.open('r') as f:
            #     contents = f.read()
            #     print(contents,'*********************************')

            send_mail_on_share_candidate_cv(user,users,encoded_file,file_name)
            return Response( status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
