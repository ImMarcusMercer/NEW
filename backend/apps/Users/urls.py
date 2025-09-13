# backend/api/urls.py
from django.urls import path
from .views import UserLoginAPIView, PromoteToOfficerAPIView, DemoteOfficerAPIView

urlpatterns = [
    # Points to UserLoginAPI, to handle authentication
    path('login/api/', UserLoginAPIView.as_view(), name='user-login'),
    path("roles/org-officer/<int:user_id>/promote/", PromoteToOfficerAPIView.as_view()),
    path("roles/org-officer/<int:user_id>/demote/",  DemoteOfficerAPIView.as_view()),
]
