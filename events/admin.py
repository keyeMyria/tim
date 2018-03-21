from django.contrib import admin
from . import models

@admin.register(models.Type)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):

    list_display = ('title', 'slug', 'author', 'status', 'uuid')
    list_filter = ('status', 'created', )
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',) }
    date_hierarchy = 'created'
    ordering = ['status', 'created']

    def get_form(self, request, obj=None, **kwargs):
        form = super(EventAdmin, self).get_form(request, obj=obj, **kwargs)
        form.request = request
        form.base_fields['author'].initial = request.user.id
        return form

