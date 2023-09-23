from django.urls import path

from . import views

urlpatterns = [
    # candidate urls
    path(r'candidates', views.CandidateCreateAPIView.as_view()),
    path(r'candidates/<int:pk>', views.CandidateRetrieveUpdateAPIView.as_view()),
    path(r'candidates/<int:pk>/activate', views.CandidateActivateAPIView.as_view()),
    path(r'candidates/<int:pk>/deactivate', views.CandidateDeactivateAPIView.as_view()),
    path(r'candidates/all', views.AllCandidatesListAPIView.as_view()),
    path(r'candidates/validate_email', views.ValidateEmailAPIView.as_view()),
    path(r'candidates/getCV/<int:pk>', views.CandidateRetrieveUpdateAPIView.as_view()),
    path(r'candidates/shareCv', views.ShareCandidateCVAPIView.as_view()),

     #path(r'candidates_language/<int:pk>', views.CandidateLanguageRetrieveUpdateAPIView.as_view()),
     #path(r'candidates/candidates_language/', views.CandidateLanguageCreateAPIView.as_view()),

    # contact urls
    path(r'candidates/language_details/', views.LanguageDetailCreateAPIView.as_view()),
    path(r'candidates/language_details/<int:pk>', views.LanguageDetailRetrieveUpdateAPIView.as_view()),

    # key words urls
    path(r'key_words/', views.KeyWordsCreateAPIView.as_view()),
    path(r'key_words/<int:pk>', views.KeyWordsRetrieveUpdateAPIView.as_view()),
    path(r'key_words/list', views.AllKeyWordsList.as_view()),

    # documents routes
    path(r'candidate/documents/<int:pk>', views.DocumentRetrieveUpdateAPIView.as_view()),
    path(r'candidate/documents/', views.DocumentRetrieveCreateAPIView.as_view()),
    path(r'documents/getCV/<int:pk>', views.GetCVAPIView.as_view()),
    path(r'document/download/<int:pk>', views.DownloadDocumentAPIViews.as_view())

]
