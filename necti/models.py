from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from users.models import Account
import hashlib
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from taggit.managers import TaggableManager
from common.models import Comment, GeoLocation
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



class KillChain(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Intentsion(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class ObservableType(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Observable(models.Model):
    name = models.CharField(max_length=250)
    notes = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=250, unique_for_date='created', null=True)
    author = models.ForeignKey(Account, null=True, related_name='observable_author')
    kill_chain = models.ManyToManyField(KillChain, related_name='obs_kill_chain', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    first_seen = models.DateTimeField(null=True, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    blacklist = models.BooleanField(default=False)
    malware_eradication = models.BooleanField(default=False)
    vurnerability_management = models.BooleanField(default=False)
    to_ids = models.NullBooleanField(default=None)
    sharing = models.BooleanField(default=True)
    rateing = models.PositiveSmallIntegerField(default=0,
                                               validators=[
                                                    MaxValueValidator(100),
                                                    MinValueValidator(0)
                                               ])

    def __str__(self):
        return self.name

class AliasField(models.Field):
    def contribute_to_class(self, cls, name, virtual_only=False):
        super(AliasField, self).contribute_to_class(cls, name, virtual_only=True)
        setattr(cls, name, self)
    
    def __get__(self, instance, instance_type=None):
        return getattr(instance, self.db_column)


class ObservableValue(models.Model):
    value = models.CharField(max_length=25)
    value_md5 = models.CharField(max_length=255, editable=False )
    obs_type = models.ForeignKey(ObservableType, related_name='types')
    observable = models.ForeignKey(Observable, related_name='types', null=True)
    values = AliasField()

    def save(self, *args, **kwargs):        
        self.value_md5 = hashlib.md5(self.value).hexdigest()
        super(ObservableValue, self).save(*args, **kwargs)

    def __str__(self):
        return self.value



class Motive(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class Sector(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class TTPCategory(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'TTP Category'
        verbose_name_plural = "TTP Categories" 

    def __str__(self):
        return self.name

class TTPType(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'TTP Type'
        verbose_name_plural = "TTP Types" 

    def __str__(self):
        return self.name

class TTP(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    author = models.ForeignKey(Account, related_name='ttp_author', null=True)
    category = models.ForeignKey(TTPCategory, related_name='ttp_category', null=True)  
    ttp_type = models.ForeignKey(TTPType, related_name='ttp_type', null=True)  
    reference = models.CharField(max_length=250, null=True, blank=True)
    hunting = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    kill_chain = models.ManyToManyField(KillChain, related_name='ttp_kill_chain', blank=True)
    intention = models.ManyToManyField(Intentsion, related_name='ttp_intention', blank=True)
    first_seen = models.DateTimeField(null=True, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'TTP'
        verbose_name_plural = "TTPs" 
    def __str__(self):
        return self.name

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


class Subject(models.Model):
    name = models.CharField(max_length=250, unique=True)
    acronym = models.CharField(max_length=250, unique=True)
    description = models.TextField(null=True, blank=True)
    subject_type = models.ForeignKey(SubjectType, related_name='subject_type', null=True)
    
    def __str__(self):
        return self.name

class ThreatActorAlias(models.Model):
    author = models.ForeignKey(Subject, null=True)
    alias = models.CharField(max_length=250, unique=True)

    class Meta:
        verbose_name_plural = "Threat actor aliases"

class ThreatActorType(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class ThreatActor(models.Model):
    name = models.CharField(max_length=250, unique=True)
    author = models.ForeignKey(Account, related_name='threat_actor_author', null=True)
    motive = models.ForeignKey(Motive, related_name='ta_motive', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    ta_type = models.ForeignKey(ThreatActorType, related_name='ta_type', null=True)
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

class ThreatActorSources(models.Model):
    ta_sources = models.ForeignKey(Subject, related_name='ta_sources', null=True)
    threat_source = models.ForeignKey(ThreatActor, related_name='source_ta', null=True, blank=True)

class TAGeoLocation(GeoLocation):
    ta_geoloc = models.ForeignKey(ThreatActor, related_name='ta_geoloc', null=True, blank=True)

class ThreatActorAliasCon(models.Model):
    threat_actor = models.ForeignKey(ThreatActor, related_name='taa_threat_actor')
    alias = models.ForeignKey(ThreatActorAlias, related_name='taa_alias')

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
    document = models.FileField(upload_to='documents/events/', null=True, blank=True)

    confidence = models.CharField(max_length=10, choices=LEVELS, default='unknown')
    risk = models.CharField(max_length=10, choices=LEVELS, default='unknown')
    event_type = models.ForeignKey(EventType, related_name='ev_type', null=True)
    tlp = models.CharField(max_length=10, choices=TLP, default='red')

    rateing = models.PositiveSmallIntegerField(default=0,
                                               validators=[MaxValueValidator(100),
                                                           MinValueValidator(0)])

    reference = models.CharField(max_length=250, null=True, blank=True)
    tag = TaggableManager() 
   

 
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('necti:event_detail', args=[self.created.year,
                                                   self.slug])
        #return reverse('necti:event_detail', args=[self.id])




class EventComment(Comment):
    event = models.ForeignKey(Event, related_name='event_comments', null=True, blank=True)

class EventGeoLocation(GeoLocation):
    location = models.ForeignKey(Event, related_name='ev_geoloc', null=True, blank=True)

class EventMotive(models.Model):
    motive = models.ForeignKey(Motive, related_name='ev_motive', null=True, blank=True)
    event = models.ForeignKey(Event, related_name='motive_ev', null=True, blank=True)

class EventSector(models.Model):
    sector = models.ForeignKey(Sector, related_name='ev_sector', null=True, blank=True)
    event = models.ForeignKey(Event, related_name='sector_ev', null=True, blank=True)

class EventThreatActor(models.Model):
    threat_actor = models.ForeignKey(ThreatActor, related_name='ev_threat_actor', null=True, blank=True)
    event = models.ForeignKey(Event, related_name='threat_actor_ev', null=True, blank=True)

class EventTTP(models.Model):
    ttp = models.ForeignKey(TTP, related_name='ev_ttp', null=True, blank=True)
    event = models.ForeignKey(Event, related_name='ttp_ev', null=True, blank=True)

class EventReporter(models.Model):
    reporter = models.ForeignKey(Reporter, related_name='ev_reporter', null=True, blank=True)
    event = models.ForeignKey(Event, related_name='reporter_ev', null=True, blank=True)

class EventObservable(models.Model):
    observable = models.ForeignKey(Observable, related_name='ev_observable', null=True, blank=True)
    event = models.ForeignKey(Event, related_name='observable_ev', null=True, blank=True)

class IncidentFunction(models.Model):
    name = models.CharField(max_length=25, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

class EffectRateing(models.Model):
    rateing = models.CharField(max_length=25, null=True)
    description = models.TextField(null=True, blank=True)

class Incident(models.Model):
    REPORTER = (
                ('client', 'client'),
               )
    STATUS = (
                ('new', 'new'),
                ('open', 'open'),
                ('resolved', 'resolved')
            )
    title = models.CharField(max_length=250)
    rtir_ref_id = models.PositiveIntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    author = models.ForeignKey(Account, related_name='incident_author', null=True)
    owner = models.ForeignKey(Account, related_name='inci_owner_account')
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    function = models.ForeignKey(IncidentFunction, related_name='inci_account')
    effect_rateing = models.ForeignKey(EffectRateing, related_name='inci_eff_rateing')
    impact_rateing = models.ForeignKey(EffectRateing, related_name='inci_imp_rateing')
    objects = models.Manager() # The default manager.
    organization = PublishedManager() # The Dahl-specific manager.
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    reporter = models.CharField(max_length=10, choices=REPORTER, default='client')
    due_date = models.DateTimeField(null=True, blank=True)

    def time_spent(self):
        time_spent = 0
        if self.start and self.end:
            time_spent = self.end - self.start
        return time_spent

class IncidentValue(models.Model):
    value = models.CharField(max_length=25)
    obs_type = models.ForeignKey(ObservableType, related_name='inci_obs_types')
    incident = models.ForeignKey(Incident, related_name='incident_value', null=True)

    def __str__(self):
        return self.value


