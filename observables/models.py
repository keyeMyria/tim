from django.db import models
from django.utils import timezone
from django.urls import reverse
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


class ObservableType(models.Model):
    TYPES = (
        ('ip_type', 'IP'),
        ('string_type', 'String'),
        ('email_type', 'Email'),
        ('file_type', 'File'),
    )

    name = models.CharField(max_length=25)
    description = models.TextField(null=True, blank=True)
    type_class = models.CharField(max_length=25, choices=TYPES, default=None)

    def __str__(self):
        typ_class = self.type_class
        for typ in self.TYPES:
            if self.type_class in typ:
                typ_class = typ[1]
        if self.name == typ_class:
            return self.name
        else:
            return "%s | %s" % (typ_class, self.name)



class Observable(models.Model):
    name = models.CharField(max_length=250, unique=True)
    notes = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=250, null=True, unique=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, related_name='observable_author')
    kill_chain = models.ForeignKey(KillChain, on_delete=models.SET_NULL, related_name='obs_kill_chain', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True)
    first_seen = models.DateTimeField(null=True, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False, unique=True)
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

    confidence = models.CharField(max_length=10, choices=CONFIDENCE, default='unknown')
    risk = models.CharField(max_length=10, choices=LEVELS, default='unknown')
    tlp = models.CharField(max_length=10, choices=TLP, default='red')


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('observables:observable_detail', args=[self.pk, self.uuid])


class ObservableValueManager(models.Manager):
    def value(self, type_id):
        return ObservableType.objects.get(id=type_id).type_class

class IpValue(models.Model):
    value = models.GenericIPAddressField(null=True, blank=True, unique=True)

    def __str__(self):
        return self.value


class EmailValue(models.Model):
    value = models.EmailField(null=True, blank=True, unique=True)

    def __str__(self):
        return self.value

class StringValue(models.Model):
    value = models.CharField(max_length=25, blank=True, unique=True)

    def __str__(self):
        return self.value

class ObservableValues(models.Model):
    observable = models.ForeignKey(Observable, null=True, blank=True, on_delete=models.SET_NULL, related_name='values')
    ip = models.ForeignKey(IpValue, null=True, blank=True, on_delete=models.SET_NULL, related_name='obs_values')
    email = models.ForeignKey(EmailValue, null=True, blank=True, on_delete=models.SET_NULL, related_name='obs_values')
    string = models.ForeignKey(StringValue, null=True, blank=True, on_delete=models.SET_NULL, related_name='obs_values')
    type = models.ForeignKey(ObservableType, on_delete=models.CASCADE, related_name='observable_value', null=True)

    def __str__(self):
        return "Test"





class FileValue(models.Model):
    str_type = models.ForeignKey(ObservableType, on_delete=models.CASCADE, related_name='file_value', null=True)
    file_value = models.ForeignKey(Observable, on_delete=models.CASCADE, related_name="file_value", null=True)

    value = models.FileField(upload_to='documents/observables/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.value

