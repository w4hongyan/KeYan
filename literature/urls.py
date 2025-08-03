from django.urls import path
from .views import JournalListCreateView, JournalRetrieveUpdateDestroyView, LiteratureListCreateView, LiteratureRetrieveUpdateDestroyView, LiteratureUserListCreateView, LiteratureUserRetrieveUpdateDestroyView
from .pubmed_views import PubMedSearchView, PubMedDetailView, PubMedBatchView, PubMedStatsView
from .translation_views import TranslationView, LiteratureTranslationView, BatchTranslationView, TranslationConfigView
from .file_upload_views import FileUploadView, FileListView, FileDeleteView, FileUploadConfigView
from .notification_views import NotificationListView, NotificationReadView, NotificationUnreadCountView, NotificationTestView

urlpatterns = [
    path('journals/', JournalListCreateView.as_view(), name='journal-list-create'),
    path('journals/<int:pk>/', JournalRetrieveUpdateDestroyView.as_view(), name='journal-detail'),
    path('literatures/', LiteratureListCreateView.as_view(), name='literature-list-create'),
    path('literatures/<int:pk>/', LiteratureRetrieveUpdateDestroyView.as_view(), name='literature-detail'),
    path('literature-users/', LiteratureUserListCreateView.as_view(), name='literature-user-list-create'),
    path('literature-users/<int:pk>/', LiteratureUserRetrieveUpdateDestroyView.as_view(), name='literature-user-detail'),
    
    # PubMed API
    path('pubmed/search/', PubMedSearchView.as_view(), name='pubmed-search'),
    path('pubmed/detail/<str:pmid>/', PubMedDetailView.as_view(), name='pubmed-detail'),
    path('pubmed/batch/', PubMedBatchView.as_view(), name='pubmed-batch'),
    path('pubmed/stats/', PubMedStatsView.as_view(), name='pubmed-stats'),
    
    # Translation API
    path('translate/text/', TranslationView.as_view(), name='translate-text'),
    path('translate/literature/', LiteratureTranslationView.as_view(), name='translate-literature'),
    path('translate/batch/', BatchTranslationView.as_view(), name='translate-batch'),
    path('translate/config/', TranslationConfigView.as_view(), name='translate-config'),
    
    # File Upload API
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('upload/files/', FileListView.as_view(), name='file-list'),
    path('upload/files/<str:filename>/', FileDeleteView.as_view(), name='file-delete'),
    path('upload/config/', FileUploadConfigView.as_view(), name='file-upload-config'),
    
    # Notification API
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/read/', NotificationReadView.as_view(), name='notification-read'),
    path('notifications/unread-count/', NotificationUnreadCountView.as_view(), name='notification-unread-count'),
    path('notifications/test/', NotificationTestView.as_view(), name='notification-test'),
]