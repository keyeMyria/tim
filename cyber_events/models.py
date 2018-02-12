from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from users.models import Account
import hashlib
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from taggit.managers import TaggableManager

from common.models import Comment, Motive, Sector, Reporter
from django_countries.fields import CountryField
from common.managers import UserAccountManager, PublishedManager, ClientsManager

LEVELS = (
    ('critical', 'critical'),
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

class EventType(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='created')
    author = models.ForeignKey(Account, related_name='event_author', null=True)
    description = models.TextField(null=True, blank=True)
    event_date = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)

    objects = models.Manager() # The default manager.
    published = PublishedManager() # The Dahl-specific manager.

    confidence = models.CharField(max_length=10, choices=LEVELS, default='unknown')
    risk = models.CharField(max_length=10, choices=LEVELS, default='unknown')
    event_type = models.ForeignKey(EventType, related_name='ev_type', null=True)
    tlp = models.CharField(max_length=10, choices=TLP, default='red')

    rateing = models.PositiveSmallIntegerField(default=0,
                                               validators=[MaxValueValidator(100),
                                                           MinValueValidator(0)])

    reference = models.CharField(max_length=250, null=True, blank=True)
    country = CountryField(null=True)
    motive = models.ForeignKey(Motive, related_name='event_motive', null=True, blank=True)
    sector = models.ForeignKey(Sector, related_name='ev_sector', null=True, blank=True)
    reporter = models.ForeignKey(Reporter, related_name='ev_reporter', null=True, blank=True)
    tag = TaggableManager() 
   
 
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('cyber_events:event_detail', args=[self.created.year,
                                                   self.slug])

class EventDocument(models.Model):
    event = models.ForeignKey(Event, related_name='event_document', null=True, blank=True)
    title = models.CharField(max_length=25)
    doc_type = models.CharField(max_length=25)
    description = models.TextField(null=True, blank=True)
    document = models.FileField(upload_to='documents/events/', null=True, blank=True)

    def __str__(self):
        return self.title


class EventComment(Comment):
    event = models.ForeignKey(Event, related_name='event_comments', null=True, blank=True)


#class EventThreatActor(models.Model):
#    threat_actor = models.ForeignKey(ThreatActor, related_name='ev_threat_actor', null=True, blank=True)
#    event = models.ForeignKey(Event, related_name='threat_actor_ev', null=True, blank=True)
#
#class EventTTP(models.Model):
#    ttp = models.ForeignKey(TTP, related_name='ev_ttp', null=True, blank=True)
#    event = models.ForeignKey(Event, related_name='ttp_ev', null=True, blank=True)


#class EventObservable(models.Model):
#    observable = models.ForeignKey(Observable, related_name='ev_observable', null=True, blank=True)
#    event = models.ForeignKey(Event, related_name='observable_ev', null=True, blank=True)

