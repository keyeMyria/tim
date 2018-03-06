from __future__ import unicode_literals

from django.db import models
from users.models import Account
from django_countries.fields import CountryField
from django.urls import reverse

LEVELS = (
    ('critical', 'critical'),
    ('high', 'high'),
    ('medium', 'medium'),
    ('low', 'low'),
    ('unknown', 'unknown'),
)

class Comment(models.Model):
    author = models.ForeignKey(Account, null=True, related_name='comment_author', on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True)
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
    author = models.ForeignKey(Account, null=True, related_name='motive', on_delete=models.CASCADE)
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('common:motive_detail', args=[self.pk])

class SectorClass(models.Model):
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(null=True, blank=True)
    author = models.ForeignKey(Account, null=True, related_name='sector_class', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('common:sector_detail', args=[self.pk])


class Sector(models.Model):
    sector_class = models.ManyToManyField(SectorClass, related_name='sector')
    name = models.CharField(max_length=250, unique=True)
    author = models.ForeignKey(
            Account, null=True, related_name='sector', on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=LEVELS, default='draft')
    nis = models.BooleanField(default=False)
    constituent = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('common:sector_detail', args=[self.pk])

class Reporter(models.Model):
    author = models.ForeignKey(Account, null=True, related_name='reporter', on_delete=models.CASCADE)
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class SubjectType(models.Model):
    author = models.ForeignKey(Account, null=True, related_name='subject_type', on_delete=models.CASCADE)
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

# Subject in in this case is the general Organization or Person
class Subject(models.Model):
    author = models.ForeignKey(Account, null=True, related_name='subject', on_delete=models.CASCADE)
    name = models.CharField(max_length=250, unique=True)
    acronym = models.CharField(max_length=250, unique=True)
    description = models.TextField(null=True, blank=True)
    subject_type = models.ForeignKey(SubjectType, related_name='subject_type', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class KillChain(models.Model):
    author = models.ForeignKey(Account, null=True, related_name='kill_chain', on_delete=models.CASCADE)
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

# Intentsion, under TTP (" what is this TTPs intentsion, what is the effect. ")
class Intentsion(models.Model):
    author = models.ForeignKey(Account, null=True, related_name='intentsion', on_delete=models.CASCADE)
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('common:intentsion_detail', args=[self.pk])


