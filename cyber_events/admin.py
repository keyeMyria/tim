from django.contrib import admin
import models

# Inlines 
#class EventObservableInline(admin.TabularInline):
#    model = models.EventObservable
#    extra = 1

class EventCommentsInline(admin.TabularInline):
    model = models.EventComment
    extra = 0

#class ObservableValueInline(admin.TabularInline):
#    model = models.ObservableValue
#    extra = 1

#class EventThreatActorInline(admin.TabularInline):
#    model = models.EventThreatActor
#    extra = 1

class EventGeoLocationInline(admin.TabularInline):
    model = models.EventGeoLocation
    extra = 0

#class ThreatActorSourcesInline(admin.TabularInline):
#    model = models.ThreatActorSources
#    extra = 0

#@admin.register(models.ObservableType)
#class ObservableTypeAdmin(admin.ModelAdmin):
#    list_display = ('name', 'description')
#
#@admin.register(models.Observable)
#class ObservableAdmin(admin.ModelAdmin):
#    list_display = ('name', 'notes', 'uuid')
#    inlines = [ObservableValueInline]

@admin.register(models.EventType)
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

    #inlines = [EventObservableInline, EventThreatActorInline, EventGeoLocationInline, EventCommentsInline]
    inlines = [EventGeoLocationInline, EventCommentsInline]
    def get_form(self, request, obj=None, **kwargs):
        form = super(EventAdmin, self).get_form(request, obj=obj, **kwargs)
        form.request = request
        form.base_fields['author'].initial = request.user.id
        return form


#@admin.register(models.KillChain)
#class KillChainAdmin(admin.ModelAdmin):
#    list_display = ('name', 'description')
#
#@admin.register(models.Intentsion)
#class IntentAdmin(admin.ModelAdmin):
#    list_display = ('name', 'description')
#
#@admin.register(models.Motive)
#class MotiveAdmin(admin.ModelAdmin):
#    list_display = ('name', 'description')
#
#@admin.register(models.Sector)
#class SectorAdmin(admin.ModelAdmin):
#    list_display = ('name', 'description')
#
#@admin.register(models.TTPCategory)
#class TTPCategoryAdmin(admin.ModelAdmin):
#    list_display = ('name', 'description')
#
#@admin.register(models.TTPType)
#class TTPTypeAdmin(admin.ModelAdmin):
#    list_display = ('name', 'description')
#
#@admin.register(models.TTP)
#class TTPAdmin(admin.ModelAdmin):
#    list_display = ('name', 'description')
#
#@admin.register(models.Reporter)
#class ReporterAdmin(admin.ModelAdmin):
#    list_display = ('name', 'description')
#
#@admin.register(models.SubjectType)
#class SubjectTypeAdmin(admin.ModelAdmin):
#    list_display = ('name', 'description')
#
#@admin.register(models.Subject)
#class SubjectAdmin(admin.ModelAdmin):
#    list_display = ('name', 'description')
#
#@admin.register(models.ThreatActorAlias)
#class ThreatActorAliasAdmin(admin.ModelAdmin):
#    list_display = ('author', 'alias' )
#
#@admin.register(models.ThreatActorType)
#class ThreatActorTypeAdmin(admin.ModelAdmin):
#    list_display = ('name', 'description')
# 
#@admin.register(models.ThreatActor)
#class ThreatActorAdmin(admin.ModelAdmin):
#    list_display = ('name', 'description', 'ta_type' )
#    inlines = [ThreatActorSourcesInline]
