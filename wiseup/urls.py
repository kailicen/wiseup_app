from django.urls import path

from . import views
from .views import (
    QuestionListView, UserQuestionListView, UserAnswerListView, 
    QuestionDetailView, 
    QuestionCreateView, AnswerCreateView, 
    QuestionUpdateView, AnswerUpdateView, 
    QuestionDeleteView, AnswerDeleteView
)

urlpatterns = [
    path('', QuestionListView.as_view(), name='wiseup-home'),
    path('user-questions/<str:username>/', UserQuestionListView.as_view(), name='user-questions'),
    path('user-answers/<str:username>/', UserAnswerListView.as_view(), name='user-answers'),
    path('question/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
    path('question/new/', QuestionCreateView.as_view(), name='question-create'),
    path('answer/new/<int:pk>/', AnswerCreateView.as_view(), name='answer-create'),
    path('question/<int:pk>/update/', QuestionUpdateView.as_view(), name='question-update'),
    path('answer/<int:pk>/update/', AnswerUpdateView.as_view(), name='answer-update'),
    path('question/<int:pk>/delete/', QuestionDeleteView.as_view(), name='question-delete'),
    path('answer/<int:pk>/delete/', AnswerDeleteView.as_view(), name='answer-delete'),

    path('about/', views.about, name='wiseup-about'),
]
