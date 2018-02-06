from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.views import generic
import logging

logger = logging.getLogger(__name__)

class IndexView(LoginRequiredMixin, generic.View):
    template_name = 'index/index.html'
    def get(self, request):
        return render(request, 'index/index.html')
