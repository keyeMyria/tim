# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
import models

# Register your models here.

# Inlines 
class IpValueInline(admin.TabularInline):
    model = models.IpValueSelect
    extra = 0 

@admin.register(models.IpValue)
class ObservableAdmin(admin.ModelAdmin):
    list_display = ('value',)

@admin.register(models.Observable)
class ObservableAdmin(admin.ModelAdmin):
    list_display = ('name', 'notes')

@admin.register(models.ObservableType)
class ObservableTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(models.ObservableValue)
class ObservableValueAdmin(admin.ModelAdmin):
    list_display = ('observable', )
    inlines = [IpValueInline]
