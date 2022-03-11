from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from .views import *
from mainApp.apis.training_session_api import TrainingSessionApi

urlpatterns = [
    path("dashboard", dashboard_view),
    path("dashboard/add_training_session", add_trs_view),
    path("trs/<int:trs_id>", TrainingSessionApi.as_view())
]