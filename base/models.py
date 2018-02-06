from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    def __unicode__(self):
        return self.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def handle_user_save(sender, instance=None, created=False, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        Token.objects.create(user=instance)


