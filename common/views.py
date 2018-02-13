# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.views import generic, View
from django.core.mail import send_mail
from django.db.models import Count
from django.views.generic.edit import FormMixin
from taggit.models import Tag

from django.http import HttpResponseForbidden
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import DetailView, UpdateView, CreateView
from django.http import HttpResponseRedirect

import models
from users.models import User
from users.views import UserCanViewDataMixin


from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class MotiveListView(UserCanViewDataMixin, ListView):
    context_object_name = 'motives'
    paginate_by = 30
    template_name_suffix = '_list'
    model = models.Motive


class MotiveCreateView(UserCanViewDataMixin, CreateView):
    #form_class = ObservableEditForm
    template_name_suffix = '_create'
    model = models.Motive
    fields = '__all__'

    def get_success_url(self):
       return reverse('common:motive_list')


class MotiveDisplayView(DetailView):
    model = models.Motive
    template_name_suffix = '_detail'

    def get_context_data(self, **kwargs):
        context = super(MotiveDisplayView, self).get_context_data(**kwargs)
        mot_id = kwargs['object'].id
        motive = get_object_or_404(self.model, id=mot_id)

        
        context = {'motive': motive,
                  }

        return context


class MotiveDetailView(View):

    def get(self, request, *args, **kwargs):
        view = MotiveDisplayView.as_view()
        return view(request, *args, **kwargs)


class MotiveEditView(UserCanViewDataMixin, UpdateView):
    model = models.Motive
    template_name_suffix = '_create'
    is_update_view = True
    fields = '__all__'

    def get_success_url(self):
        return reverse('common:motive_detail', kwargs={'pk' : self.object.pk})

    def get_object(self, queryset=None):
       object = super(MotiveEditView, self).get_object()
       user = self.request.user
       if user.is_superuser:
           return object
       else:
           org = user.account.organization
           if org == object.account.organization and user.is_staff:
               return object
           raise PermissionDenied('Not allowed')


class MotiveDeleteView(UserCanViewDataMixin, DeleteView):
    model = models.Motive
    template_name_suffix = '_delete'
    success_url = reverse_lazy('common:motive_list')


# --- Sector ---

class SectorListView(UserCanViewDataMixin, ListView):
    context_object_name = 'objects'
    paginate_by = 30
    template_name_suffix = '_list'
    model = models.Sector


class SectorCreateView(UserCanViewDataMixin, CreateView):
    #form_class = ObservableEditForm
    template_name_suffix = '_create'
    model = models.Sector
    fields = '__all__'

    def get_success_url(self):
       return reverse('common:sector_list')


class SectorDisplayView(DetailView):
    model = models.Sector
    template_name_suffix = '_detail'

    def get_context_data(self, **kwargs):
        context = super(SectorDisplayView, self).get_context_data(**kwargs)
        sec_id = kwargs['object'].id
        sector = get_object_or_404(self.model, id=sec_id)

        
        context = {'object': sector,
                  }

        return context


class SectorDetailView(View):

    def get(self, request, *args, **kwargs):
        view = SectorDisplayView.as_view()
        return view(request, *args, **kwargs)


class SectorEditView(UserCanViewDataMixin, UpdateView):
    model = models.Sector
    template_name_suffix = '_create'
    is_update_view = True
    fields = '__all__'

    def get_success_url(self):
        return reverse('common:sector_detail', kwargs={'pk' : self.object.pk})

    def get_object(self, queryset=None):
       object = super(SectorEditView, self).get_object()
       user = self.request.user
       if user.is_superuser:
           return object
       else:
           org = user.account.organization
           if org == object.account.organization and user.is_staff:
               return object
           raise PermissionDenied('Not allowed')


class SectorDeleteView(UserCanViewDataMixin, DeleteView):
    model = models.Sector
    template_name_suffix = '_delete'
    success_url = reverse_lazy('common:sector_list')


# --- Intentsion ---

class IntentsionListView(UserCanViewDataMixin, ListView):
    context_object_name = 'objects'
    paginate_by = 30
    template_name_suffix = '_list'
    model = models.Intentsion


class IntentsionCreateView(UserCanViewDataMixin, CreateView):
    #form_class = ObservableEditForm
    template_name_suffix = '_create'
    model = models.Intentsion
    fields = '__all__'

    def get_success_url(self):
       return reverse('common:intentsion_list')


class IntentsionDisplayView(DetailView):
    model = models.Intentsion
    template_name_suffix = '_detail'

    def get_context_data(self, **kwargs):
        context = super(IntentsionDisplayView, self).get_context_data(**kwargs)
        sec_id = kwargs['object'].id
        intentsion = get_object_or_404(self.model, id=sec_id)

        
        context = {'object': intentsion,
                  }

        return context


class IntentsionDetailView(View):

    def get(self, request, *args, **kwargs):
        view = IntentsionDisplayView.as_view()
        return view(request, *args, **kwargs)


class IntentsionEditView(UserCanViewDataMixin, UpdateView):
    model = models.Intentsion
    template_name_suffix = '_create'
    is_update_view = True
    fields = '__all__'

    def get_success_url(self):
        return reverse('common:intentsion_detail', kwargs={'pk' : self.object.pk})

    def get_object(self, queryset=None):
       object = super(IntentsionEditView, self).get_object()
       user = self.request.user
       if user.is_superuser:
           return object
       else:
           org = user.account.organization
           if org == object.account.organization and user.is_staff:
               return object
           raise PermissionDenied('Not allowed')


class IntentsionDeleteView(UserCanViewDataMixin, DeleteView):
    model = models.Intentsion
    template_name_suffix = '_delete'
    success_url = reverse_lazy('common:intentsion_list')


# --- KillChain ---

class KillChainListView(UserCanViewDataMixin, ListView):
    context_object_name = 'objects'
    paginate_by = 30
    template_name_suffix = '_list'
    model = models.KillChain


class KillChainCreateView(UserCanViewDataMixin, CreateView):
    #form_class = ObservableEditForm
    template_name_suffix = '_create'
    model = models.KillChain
    fields = '__all__'

    def get_success_url(self):
       return reverse('common:killchain_list')


class KillChainDisplayView(DetailView):
    model = models.KillChain
    template_name_suffix = '_detail'

    def get_context_data(self, **kwargs):
        context = super(KillChainDisplayView, self).get_context_data(**kwargs)
        sec_id = kwargs['object'].id
        killchain = get_object_or_404(self.model, id=sec_id)

        
        context = {'object': killchain,
                  }

        return context


class KillChainDetailView(View):

    def get(self, request, *args, **kwargs):
        view = KillChainDisplayView.as_view()
        return view(request, *args, **kwargs)


class KillChainEditView(UserCanViewDataMixin, UpdateView):
    model = models.KillChain
    template_name_suffix = '_create'
    is_update_view = True
    fields = '__all__'

    def get_success_url(self):
        return reverse('common:killchain_detail', kwargs={'pk' : self.object.pk})

    def get_object(self, queryset=None):
       object = super(KillChainEditView, self).get_object()
       user = self.request.user
       if user.is_superuser:
           return object
       else:
           org = user.account.organization
           if org == object.account.organization and user.is_staff:
               return object
           raise PermissionDenied('Not allowed')


class KillChainDeleteView(UserCanViewDataMixin, DeleteView):
    model = models.KillChain
    template_name_suffix = '_delete'
    success_url = reverse_lazy('common:killchain_list')

