from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, AnswerViewSet, TagViewSet

router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'answers', AnswerViewSet, basename='answer')
router.register(r'tags', TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router.urls)),
    path('questions/<int:pk>/answers/', 
         AnswerViewSet.as_view({'get': 'list', 'post': 'create'}), 
         name='question-answers'),
    path('questions/<int:pk>/upvote/', 
         QuestionViewSet.as_view({'post': 'upvote'}), 
         name='question-upvote'),
    path('questions/<int:pk>/downvote/', 
         QuestionViewSet.as_view({'post': 'downvote'}), 
         name='question-downvote'),
    path('answers/<int:pk>/upvote/', 
         AnswerViewSet.as_view({'post': 'upvote'}), 
         name='answer-upvote'),
    path('questions/<int:pk>/collect/', 
         QuestionViewSet.as_view({'post': 'collect'}), 
         name='question-collect'),
    path('answers/<int:pk>/accept/', 
         AnswerViewSet.as_view({'post': 'accept'}), 
         name='answer-accept'),
]