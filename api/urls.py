from django.urls import path
from .views import (
    UserRegistrationView, UserLoginView, UserRefreshTokenView, UserProfileView,
    UserProfileDetailView, UserAvatarUploadView, BillingInfoView, BillingInfoDetailView
)
from .views_statistics import StatisticsView

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
]
