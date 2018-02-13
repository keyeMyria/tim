# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from common.models import Motive
from users.models import Account
from django.core.urlresolvers import reverse


class ActorType(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor:actor_type_detail', args=[self.pk])


class Organization(models.Model):
    name = models.CharField(max_length=250, unique=True)
    author = models.ForeignKey(Account, related_name='constituent_author', null=True)
    description = models.TextField(null=True, blank=True)
    type = models.ForeignKey(ActorType, related_name='constituent_type', null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor:organization_detail', args=[self.pk])


class ThreatActor(models.Model):
    name = models.CharField(max_length=250, unique=True)
    author = models.ForeignKey(Account, related_name='threat_actor_author', null=True)
    motive = models.ForeignKey(Motive, related_name='threat_actor_motive', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    type = models.ForeignKey(ActorType, related_name='threat_actor_type', null=True)
    first_seen = models.DateTimeField(null=True, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    reference = models.CharField(max_length=250, null=True, blank=True)
    import_name = models.CharField(max_length=250, null=True, blank=True)
    hunting = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    document = models.FileField(upload_to='documents/threat_actor/', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor:threat_actor_detail', args=[self.pk])


#class Reporter(models.Model):
#    name = models.CharField(max_length=250, unique=True)
#    author = models.ForeignKey(Account, related_name='reporter_author', null=True)
#    description = models.TextField(null=True, blank=True)
#    type = models.ForeignKey(ActorType, related_name='reporter_type', null=True)
#    created = models.DateTimeField(auto_now_add=True)
#    updated = models.DateTimeField(auto_now=True)
#
#
#    class Meta:
#        ordering = ('-created',)
#
#    def __str__(self):
#        return self.name
#
#    def get_absolute_url(self):
#        return reverse('actor:reporter_detail', args=[self.pk])
#
#
#class Constituent(models.Model):
#    name = models.CharField(max_length=250, unique=True)
#    author = models.ForeignKey(Account, related_name='constituent_author', null=True)
#    description = models.TextField(null=True, blank=True)
#    type = models.ForeignKey(ActorType, related_name='constituent_type', null=True)
#    created = models.DateTimeField(auto_now_add=True)
#    updated = models.DateTimeField(auto_now=True)
#
#
#    class Meta:
#        ordering = ('-created',)
#
#    def __str__(self):
#        return self.name
#
#    def get_absolute_url(self):
#        return reverse('actor:constituent_detail', args=[self.pk])
