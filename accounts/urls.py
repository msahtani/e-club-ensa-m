from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from .views import *


urlpatterns = [
    path('accounts/login/', login_view, name='login'),
    path('forgotten_password/', forgot_password_view),
    path('reset_password', reset_password_view),
    path('login/', login_view, name="login_v"),
    path('logout/', logout_view),
    path('signup/', signup_view),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)