from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistrationView, UserLoginView, UserRefreshTokenView, UserProfileView,
    UserProfileDetailView, UserAvatarUploadView, BillingInfoView, BillingInfoDetailView
)
from .views_statistics import StatisticsView
from .views_research import ResearchToolsViewSet
from .views_plagiarism import PlagiarismCheckViewSet
from .views_journal import JournalImpactViewSet

# 创建路由器
router = DefaultRouter()
router.register(r'research/charts', ResearchToolsViewSet, basename='research-charts')
router.register(r'plagiarism', PlagiarismCheckViewSet, basename='plagiarism')
router.register(r'journals', JournalImpactViewSet, basename='journals')

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('token/refresh/', UserRefreshTokenView.as_view(), name='token-refresh'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/detail/', UserProfileDetailView.as_view(), name='user-profile-detail'),
    path('profile/avatar/', UserAvatarUploadView.as_view(), name='user-avatar-upload'),
    path('profile/billing/', BillingInfoView.as_view(), name='billing-info'),
    path('profile/billing/<int:pk>/', BillingInfoDetailView.as_view(), name='billing-info-detail'),
    path('statistics/', StatisticsView.as_view(), name='statistics'),
    path('', include(router.urls)),
]
