# Candidates views
from .candidate_views import CandidateCreateAPIView,\
    CandidateRetrieveUpdateAPIView,\
    CandidateActivateAPIView, \
    CandidateDeactivateAPIView, AllCandidatesListAPIView,ValidateEmailAPIView,GetCVAPIView,ShareCandidateCVAPIView

# Contacts views
from .language_detail_views import LanguageDetailRetrieveUpdateAPIView, \
    LanguageDetailCreateAPIView

# Key words views
from .key_words_views import KeyWordsCreateAPIView,KeyWordsRetrieveUpdateAPIView,AllKeyWordsList

# Documents views
from .document_views import DocumentRetrieveCreateAPIView,DocumentRetrieveUpdateAPIView,DownloadDocumentAPIViews,GetCVAPIView