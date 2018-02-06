from django.shortcuts import render

# Create your views here.
from utils import status_monitor

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.views import generic
from ahconfig.models import StartupBot
import logging

logger = logging.getLogger(__name__)

#@login_required(login_url="login")
class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'
    model = StartupBot
    template_name = 'base/index.html'
    
