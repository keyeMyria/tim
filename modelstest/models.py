# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Parent(models.Model):
    name = models.CharField(max_length=250)


class Child(models.Model):
    name = models.CharField(max_length=250)

class ParentChild(models.Model):
    parent = models.ForeignKey(Parent, related_name='child')
    child = models.ForeignKey(Child, related_name='parent', null=True)
