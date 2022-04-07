from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from .views import MembershipAPI, JoiningSessionAPI

urlpatterns =  [
    #MembershipAPI
    path('members/', MembershipAPI.as_view()),

    #JoiningSession
    path('joining_session/', JoiningSessionAPI.as_view() )

]