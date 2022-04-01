from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static

from .views import *


urlpatterns = [
    path("dashboard", dashboard_view),
    # path("club/<str:club_name>/dashboard/add_training_session", TrainingSessionApi.as_view()),
    # path("test/<str:club_name>/", ClubApi.as_view())
]