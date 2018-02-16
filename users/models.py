from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

class User(AbstractUser):
    pass

class Organization(models.Model):
    name = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Account(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='account')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0} | {1}'.format(self.user, self.organization)

class IpRange(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='ip_ranges')
    start = models.GenericIPAddressField()
    end = models.GenericIPAddressField()

    def __str__(self):
        return '{0} - {1}'.format(self.start, self.end)

class Domain(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='domains')
    domain = models.CharField(max_length=253)

    def __str__(self):
        return self.domain

class ASN(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='asns')
    asn = models.CharField(max_length=255)

    def __str__(self):
        return self.asn
