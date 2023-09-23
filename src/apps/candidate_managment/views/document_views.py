# python lib
import datetime

# django lib
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from django.conf import settings
from ..models import Candidate
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.core.generics import BulkDestroyModelView
import os
from django.conf import settings
from django.http import HttpResponse, Http404


# custom lib
from ..serializers import DocumentSerializer
from ..models import Document
from ..serializers.candidate_Document_serializer import CandidateDocumentSerializer


class DocumentRetrieveCreateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DocumentSerializer
    queryset = Document.objects.filter(deleted_at__isnull=True)


class DocumentRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CandidateDocumentSerializer
    queryset = Candidate.objects.filter(deleted_at__isnull=True)

# class  GetCVAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         id = self.request.query_params.get('id')
#         candidate=Candidate.objects.get(id=id)
#         cv=Document.objects.filter(candidate=id,type=1).values().first()
#         if cv :
#             return Response(cv.get('file'))
#         else :
#             return Response("example.pdf")

class  GetCVAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DocumentSerializer

    def get(self, request, *args, **kwargs):
        data=self.queryset
        cv=data.document_set[0]['file']
        if cv :
            return Response(cv)
        else :
            return Response("")

class DownloadDocumentAPIViews(generics.RetrieveAPIView):
    """
    DownloadDocumentAPIViews Allow to download a document file with a specific name related to his folder and tag
    """
    queryset = Document.objects.filter(deleted_at__isnull=True)
    serializer_class = DocumentSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        file_handle = instance.file.path
        document = open(file_handle, 'rb')
        response = HttpResponse(FileWrapper(document), content_type='application/pdf')
        file_name = instance.file
        print(file_name)
        response['Content-Disposition'] = 'attachment; filename={}.pdf'.format(file_name)
        return response
