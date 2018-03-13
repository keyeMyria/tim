# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from common.models import Motive
from users.models import Account
from django.urls import reverse
from ttps.models import TTP
from django_countries.fields import CountryField
from events.models import Event

LEVELS = (
    ('critical', 'critical'),
    ('high', 'high'),
    ('medium', 'medium'),
    ('low', 'low'),
    ('unknown', 'unknown'),
)

ROLES = (
    ('reporter', 'Reporter'),
    ('target', 'Target'),
    ('threat_actor', 'Threat Actor'),
    ('unknown', 'unknown')
)



class ActorType(models.Model):
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor:actor_type_detail', args=[self.pk])


class OrganizationDomain(models.Model):
    name = models.CharField(max_length=250, unique=True)
    author = models.ForeignKey(Account,
        on_delete=models.CASCADE, related_name='organization_domain', null=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    risk = models.CharField(max_length=10, choices=LEVELS, default='unknown')


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor:domain_detail', args=[self.pk])


class Organization(models.Model):
    name = models.CharField(max_length=250, unique=True)
    author = models.ForeignKey(Account,
        on_delete=models.CASCADE, related_name='constituent_author', null=True)
    motive = models.ForeignKey(Motive,
        on_delete=models.CASCADE,
        related_name='threat_actor_motive', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    type = models.ForeignKey(ActorType,
        on_delete=models.CASCADE, related_name='constituent_type', null=True)
    first_seen = models.DateTimeField(null=True, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    reference = models.CharField(max_length=250, null=True, blank=True)
    import_name = models.CharField(max_length=250, null=True, blank=True)
    hunting = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    country = CountryField(multiple=True, blank=True)
    domain = models.ForeignKey(OrganizationDomain,
        on_delete=models.CASCADE, related_name="organization", null=True)
    reference = models.CharField(max_length=250, null=True, blank=True)
    ttp = models.ManyToManyField(TTP, blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor:organization_detail', args=[self.pk])


class Actor(models.Model):
    role = models.CharField(max_length=25, choices=ROLES, default='unknown')
    actor = models.ManyToManyField(Organization, blank=False)
    event = models.ForeignKey(Event,
        related_name='actor', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = (("event", "role"),)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('actor:actor', args=[self.pk])
