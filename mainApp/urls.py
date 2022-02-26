from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from mainApp.views import *

urlpatterns = [
    path('<str:club>/create', add_post)

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)