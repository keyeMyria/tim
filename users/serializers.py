from django.contrib.auth.models import Group

from rest_framework import serializers

from . import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.User
        fields = ('url', 'username', 'email', 'groups')


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Organization
        fields = ('url', 'name')

class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Account
        fields = ('url', 'user', 'organization')

class IpRangeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.IpRange
        fields = ('url', 'organization', 'start', 'end')

class DomainSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Domain
        fields = ('url', 'organization', 'domain')

class ASNSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.ASN
        fields = ('url', 'organization', 'asn')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
