from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.SectorClass)
class ObservableTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'author')

