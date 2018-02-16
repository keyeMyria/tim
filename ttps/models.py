from django.db import models
from django.utils import timezone
from django.urls import reverse
from users.models import Account
import hashlib
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from taggit.managers import TaggableManager

from common.models import Comment, GeoLocation, Motive, Sector, Reporter, KillChain, Intentsion
from common.managers import UserAccountManager, PublishedManager, ClientsManager
from django.core.exceptions import ObjectDoesNotExist

class TTPCategory(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'TTP Category'
        verbose_name_plural = "TTP Categories" 

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ttp:ttp_category_detail', args=[self.pk])


class TTPType(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'TTP Type'
        verbose_name_plural = "TTP Types" 

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ttp:ttp_type_detail', args=[self.pk])


class TTP(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='ttp_author', null=True)
    category = models.ForeignKey(TTPCategory, on_delete=models.CASCADE, related_name='ttp_category', null=True)  
    ttp_type = models.ForeignKey(TTPType, on_delete=models.CASCADE, related_name='ttp_type', null=True)  
    reference = models.CharField(max_length=250, null=True, blank=True)
    hunting = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    kill_chain = models.ForeignKey(KillChain, on_delete=models.CASCADE, related_name='ttp_kill_chain', blank=True)
    intention = models.ForeignKey(Intentsion, on_delete=models.CASCADE, related_name='ttp_intention', blank=True)
    first_seen = models.DateTimeField(null=True, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'TTP'
        verbose_name_plural = "TTPs" 
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ttp:ttp_detail', args=[self.pk])


