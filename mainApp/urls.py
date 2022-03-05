from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from mainApp.apis import postApi

from mainApp.views import *

urlpatterns = [
    #path('<str:club_name>/create', add_post),
    path('club/<str:club_name>/', club_profile),
    path('post/<int:post_id>/update', update_post),
    path('post/<int:post_id>', postApi)

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)