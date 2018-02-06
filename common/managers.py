from django.db import models

class UserAccountManager(models.Manager):
    def get_queryset(self):
        return super(UserAccountManager, self).get_queryset().filter()

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class ClientsManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(subject_type='client')
