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

from . import models
from users.models import User
from users.views import UserCanViewDataMixin


from django.contrib.auth.models import Group
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class TTPTypeListView(UserCanViewDataMixin, ListView):
    context_object_name = 'objects'
    paginate_by = 30
    template_name_suffix = '_list'
    model = models.TTPType


class TTPTypeCreateView(UserCanViewDataMixin, CreateView):
    #form_class = ObservableEditForm
    template_name_suffix = '_create'
    model = models.TTPType
    fields = '__all__'

    def get_success_url(self):
       return reverse('ttp:ttp_type_list')


class TTPTypeDisplayView(DetailView):
    model = models.TTPType
    template_name_suffix = '_detail'

    def get_context_data(self, **kwargs):
        context = super(TTPTypeDisplayView, self).get_context_data(**kwargs)
        mot_id = kwargs['object'].id
        ttp_type = get_object_or_404(self.model, id=mot_id)

        
        context = {'ttp_type': ttp_type,
                  }

        return context


class TTPTypeDetailView(View):

    def get(self, request, *args, **kwargs):
        view = TTPTypeDisplayView.as_view()
        return view(request, *args, **kwargs)


class TTPTypeEditView(UserCanViewDataMixin, UpdateView):
    model = models.TTPType
    template_name_suffix = '_create'
    is_update_view = True
    fields = '__all__'

    def get_success_url(self):
        return reverse('ttp:ttp_type_detail', kwargs={'pk' : self.object.pk})

    def get_object(self, queryset=None):
       object = super(TTPTypeEditView, self).get_object()
       user = self.request.user
       if user.is_superuser:
           return object
       else:
           org = user.account.organization
           if org == object.account.organization and user.is_staff:
               return object
           raise PermissionDenied('Not allowed')


class TTPTypeDeleteView(UserCanViewDataMixin, DeleteView):
    model = models.TTPType
    template_name_suffix = '_delete'
    success_url = reverse_lazy('ttp:ttp_type_list')


class TTPCategoryListView(UserCanViewDataMixin, ListView):
    context_object_name = 'objects'
    paginate_by = 30
    template_name_suffix = '_list'
    model = models.TTPCategory


class TTPCategoryCreateView(UserCanViewDataMixin, CreateView):
    #form_class = ObservableEditForm
    template_name_suffix = '_create'
    model = models.TTPCategory
    fields = '__all__'

    def get_success_url(self):
       return reverse('ttp:ttp_category_list')


class TTPCategoryDisplayView(DetailView):
    model = models.TTPCategory
    template_name_suffix = '_detail'

    def get_context_data(self, **kwargs):
        context = super(TTPCategoryDisplayView, self).get_context_data(**kwargs)
        mot_id = kwargs['object'].id
        ttp_category = get_object_or_404(self.model, id=mot_id)

        
        context = {'ttp_category': ttp_category,
                  }

        return context


class TTPCategoryDetailView(View):

    def get(self, request, *args, **kwargs):
        view = TTPCategoryDisplayView.as_view()
        return view(request, *args, **kwargs)


class TTPCategoryEditView(UserCanViewDataMixin, UpdateView):
    model = models.TTPCategory
    template_name_suffix = '_create'
    is_update_view = True
    fields = '__all__'

    def get_success_url(self):
        return reverse('ttp:ttp_category_detail', kwargs={'pk' : self.object.pk})

    def get_object(self, queryset=None):
       object = super(TTPCategoryEditView, self).get_object()
       user = self.request.user
       if user.is_superuser:
           return object
       else:
           org = user.account.organization
           if org == object.account.organization and user.is_staff:
               return object
           raise PermissionDenied('Not allowed')


class TTPCategoryDeleteView(UserCanViewDataMixin, DeleteView):
    model = models.TTPCategory
    template_name_suffix = '_delete'
    success_url = reverse_lazy('ttp:ttp_category_list')

class TTPListView(UserCanViewDataMixin, ListView):
    context_object_name = 'objects'
    paginate_by = 30
    template_name_suffix = '_list'
    model = models.TTP


class TTPCreateView(UserCanViewDataMixin, CreateView):
    #form_class = ObservableEditForm
    template_name_suffix = '_create'
    model = models.TTP
    fields = '__all__'

    def get_success_url(self):
       return reverse('ttp:ttp_list')


class TTPDisplayView(DetailView):
    model = models.TTP
    template_name_suffix = '_detail'

    def get_context_data(self, **kwargs):
        context = super(TTPDisplayView, self).get_context_data(**kwargs)
        mot_id = kwargs['object'].id
        ttp = get_object_or_404(self.model, id=mot_id)

        
        context = {'ttp': ttp,
                  }

        return context


class TTPDetailView(View):

    def get(self, request, *args, **kwargs):
        view = TTPDisplayView.as_view()
        return view(request, *args, **kwargs)


class TTPEditView(UserCanViewDataMixin, UpdateView):
    model = models.TTP
    template_name_suffix = '_create'
    is_update_view = True
    fields = '__all__'

    def get_success_url(self):
        return reverse('ttp:ttp_detail', kwargs={'pk' : self.object.pk})

    def get_object(self, queryset=None):
       object = super(TTPEditView, self).get_object()
       user = self.request.user
       if user.is_superuser:
           return object
       else:
           org = user.account.organization
           if org == object.account.organization and user.is_staff:
               return object
           raise PermissionDenied('Not allowed')


class TTPDeleteView(UserCanViewDataMixin, DeleteView):
    model = models.TTP
    template_name_suffix = '_delete'
    success_url = reverse_lazy('ttp:ttp_list')

