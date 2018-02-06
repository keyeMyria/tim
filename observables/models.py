from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from users.models import Account
import hashlib
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from taggit.managers import TaggableManager

from common.models import Comment, GeoLocation, Motive, Sector, Reporter, KillChain
from common.managers import UserAccountManager, PublishedManager, ClientsManager
from django.core.exceptions import ObjectDoesNotExist


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


class ObservableType(models.Model):
    TYPES = (
        ('ip_type', 'IP'),
        ('string_type', 'String'),
        ('email_type', 'Email'),
        ('file_type', 'File'),
    )

    name = models.CharField(max_length=25)
    description = models.TextField(null=True, blank=True)
    type_class = models.CharField(max_length=10, choices=TYPES, default='string')

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

    def get_absolute_url(self):
        return reverse('observables:observable_detail', args=[self.pk, self.uuid])


class ObservableValueManager(models.Manager):
    def value(self, type_id):
        return ObservableType.objects.get(id=type_id).type_class

class IpValue(models.Model):
    value = models.GenericIPAddressField(unique=True)

    def __str__(self):
        return self.value

class StringValue(models.Model):
    value = models.CharField(max_length=25)

    def __str__(self):
        return self.value


class EmailValue(models.Model):
    value = models.EmailField(null=True)

    def __str__(self):
        return self.value

class FileValue(models.Model):
    value = models.FileField(upload_to='documents/observables/%Y/%m/%d/')

    def __str__(self):
        return self.value

class ObservableValue(models.Model):

    obs_type = models.ForeignKey(ObservableType, related_name='obs_types')
    observable = models.ForeignKey(Observable, related_name='types_obs', null=True)

    def __str__(self):
        return str(self.id)

class IpValueSelect(models.Model):
    ip = models.ForeignKey(ObservableValue, on_delete=models.CASCADE, related_name="obsip_value", null=True)
    value = models.ForeignKey(IpValue, on_delete=models.CASCADE, related_name="ipvalue_value", null=True)

    def __str__(self):
        return self.value.value



