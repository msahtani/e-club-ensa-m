from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from .views import *
from mainApp.apis.training_session_api import TrainingSessionApi
from mainApp.apis.club_api import ClubApi

urlpatterns = [
    path("dashboard", dashboard_view),
    path("club/<str:club_name>/dashboard/add_training_session", TrainingSessionApi.as_view()),
    path("test/<str:club_name>/", ClubApi.as_view())
]