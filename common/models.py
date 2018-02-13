from __future__ import unicode_literals

from django.db import models
from users.models import Account
from django_countries.fields import CountryField
from django.core.urlresolvers import reverse


class Comment(models.Model):
    author = models.ForeignKey(Account, null=True, related_name='comment_author')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
        abstract = True


class GeoLocation(models.Model):
    country = CountryField(null=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return '%s | %s' % (self.country, self.city)

    class Meta:
        abstract = True


class Motive(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('common:motive_detail', args=[self.pk])


class Sector(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('common:sector_detail', args=[self.pk])



class Reporter(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name


class SubjectType(models.Model):
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

# Subject in in this case is the general Organization or Person
class Subject(models.Model):
    name = models.CharField(max_length=250, unique=True)
    acronym = models.CharField(max_length=250, unique=True)
    description = models.TextField(null=True, blank=True)
    subject_type = models.ForeignKey(SubjectType, related_name='subject_type', null=True)
    
    def __str__(self):
        return self.name


class KillChain(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

# Intentsion, under TTP (" what is this TTPs intentsion, what is the effect. ")
class Intentsion(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('common:intentsion_detail', args=[self.pk])


