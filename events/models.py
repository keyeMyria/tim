from django.db import models
from django.utils import timezone
from django.urls import reverse
from users.models import Account
import hashlib
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from taggit.managers import TaggableManager

from common.models import Comment, Motive, Sector, Reporter
from django_countries.fields import CountryField
from common.managers import UserAccountManager, PublishedManager
from observables.models import Observable
from ttps.models import TTP
from django_countries.fields import CountryField
from django.template.defaultfilters import slugify


LEVELS = (
    ('critical', 'critical'),
    ('high', 'high'),
    ('medium', 'medium'),
    ('low', 'low'),
    ('unknown', 'unknown'),
)

CONFIDENCE = (
    ('high', 'high'),
    ('medium', 'medium'),
    ('low', 'low'),
    ('unknown', 'unknown'),
)


TLP = (
    ('red', 'red'),
    ('amber', 'amber'),
    ('green', 'green'),
    ('white', 'white'),
)

class Type(models.Model):
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('events:event_type')

class ReportersManager(models.Manager):
    def get_queryset(self):
        return super(Organization, self).get_queryset().filter(type='reporter')

class Event(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique_for_date='created',null=True, blank=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='event', null=True)
    description = models.TextField(null=True, blank=True)
    event_date = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False, unique=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='event', null=True)

    objects = models.Manager() # The default manager.
    published = PublishedManager() # The Dahl-specific manager.

    confidence = models.CharField(max_length=10, choices=CONFIDENCE, default='unknown')
    risk = models.CharField(max_length=10, choices=LEVELS, default='unknown')
    tlp = models.CharField(max_length=10, choices=TLP, default='red')

    rateing = models.PositiveSmallIntegerField(default=0,
                                               validators=[MaxValueValidator(100),
                                                           MinValueValidator(0)])

    motive = models.ManyToManyField(Motive, related_name='event', blank=True)
    sector = models.ManyToManyField(Sector, related_name='event', blank=True)
    tag = TaggableManager() 
    country = CountryField(multiple=True, blank=True)
    

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('events:event_detail', args=[self.uuid,
                                                   self.slug])

    def save(self, *args, **kwargs):
        if getattr(self, '_title_changed', True):
            self.slug = slugify(self.title)
        super(Event, self).save(*args, **kwargs)


class Reference(models.Model):
    reference = models.CharField(max_length=512, null=True, blank=True)
    event = models.ForeignKey(Event,
        on_delete=models.CASCADE,
        related_name='reference', null=True, blank=True)


class EventDocument(models.Model):
    event = models.ForeignKey(Event,
        on_delete=models.CASCADE,
        related_name='event_document', null=True, blank=True)
    title = models.CharField(max_length=25, unique=True)
    doc_type = models.CharField(max_length=25)
    description = models.TextField(null=True, blank=True)
    document = models.FileField(upload_to='documents/events/', null=True, blank=True)

    def __str__(self):
        return self.title


class EventComment(Comment):
    event = models.ForeignKey(Event,
        on_delete=models.CASCADE,
        related_name='event_comments', null=True, blank=True)


class EventTTP(models.Model):
    ttp = models.ForeignKey(TTP,
        related_name='ev_ttp', on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(Event,
        related_name='ttp_ev', on_delete=models.CASCADE, null=True, blank=True)


class EventObservable(models.Model):
    observable = models.ForeignKey(Observable,
        on_delete=models.CASCADE, related_name='event', blank=True)
    event = models.ForeignKey(Event,
        on_delete=models.CASCADE, related_name='observable', blank=True)

    class Meta:
        unique_together = (("observable", "event"),)

    def __str__(self):
        return "EO: %s | %s " % (str(self.observable), str(self.event))

