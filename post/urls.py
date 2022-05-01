from django.urls import path
from .views import ArticleApi

urlpatterns = [
    path('article/<int:article_id>', ArticleApi.as_view(), name='create_article'),
    path('club/<str:club_name>/article/create', ArticleApi.as_view(), name='create'),
]