from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CooperationPostViewSet, CooperationApplicationViewSet, SkillViewSet, UserSkillViewSet

router = DefaultRouter()
router.register(r'posts', CooperationPostViewSet, basename='cooperation-post')
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'user-skills', UserSkillViewSet, basename='user-skill')

# 嵌套路由
posts_router = DefaultRouter()
posts_router.register(r'applications', CooperationApplicationViewSet, basename='cooperation-application')

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_pk>/', include(posts_router.urls)),
    path('posts/<int:pk>/apply/', 
         CooperationPostViewSet.as_view({'post': 'apply'}), 
         name='post-apply'),
    path('posts/<int:pk>/applications/', 
         CooperationPostViewSet.as_view({'get': 'applications'}), 
         name='post-applications'),
    path('posts/<int:pk>/increment-view/', 
         CooperationPostViewSet.as_view({'post': 'increment_view'}), 
         name='post-increment-view'),
    path('user-skills/my-skills/', 
         UserSkillViewSet.as_view({'get': 'my_skills'}), 
         name='my-skills'),
    path('user-skills/recommendations/', 
         UserSkillViewSet.as_view({'get': 'recommendations'}), 
         name='skill-recommendations'),
]