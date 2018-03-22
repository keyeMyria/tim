from django.urls import path, re_path, include
from . import views

from rest_framework import routers


root = "dashboard/"
app_name="dashboard"
urlpatterns = [
    path(r'', views.DashboardView.as_view(), name = 'dashboard')

] 
