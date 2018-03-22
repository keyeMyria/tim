from django.http import HttpResponse
from django.views import generic, View
import datetime


class DashboardView(generic.TemplateView):
    template_name = 'dashboard/dashboard.html'

