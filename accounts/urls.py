from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from .views import *


url_patterns = [
    path('accounts/login/', login_view, name='login'),
    path('login/', login_view, name="login_v"),
    path('logout/', logout_view),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)