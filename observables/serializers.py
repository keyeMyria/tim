from rest_framework import serializers, fields

from . import models
from events.models import Event
from django.db import transaction

import traceback
from rest_framework.utils import model_meta


class IpValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IpValue
        fields = ('__all__')


class EmailValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EmailValue
        fields = ('__all__')


class FileValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FileValue
        fields = ('__all__')


class StringValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StringValue
        fields = ('__all__')


class ObservableTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ObservableType
        fields = ('__all__')


class EmailCustomField(serializers.EmailField):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate_empty_values(self, data):
        return (True, data)


class IpCustomField(serializers.IPAddressField):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate_empty_values(self, data):
        return (True, data)


class StringCustomField(serializers.CharField):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_representation(self, data):
        print(data)

    def validate_empty_values(self, data):
        return (True, data)


class ObservableValueSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="observables:observable-value-detail",
                    )

    observable = serializers.PrimaryKeyRelatedField(many=False, queryset=models.Observable.objects.all())
    ip = IpCustomField(protocol='both', required=False, allow_blank=True)
    email = EmailCustomField(required=False, allow_blank=True)
    string = StringCustomField(required=False, allow_blank=True)
    type = serializers.CharField(max_length=None, min_length=None, allow_blank=True, trim_whitespace=False )
    id = serializers.ReadOnlyField()

    def validate(self, attrs):
        print(attrs)
        return attrs

    class Meta:
        model = models.ObservableValue
        fields = ('__all__')

    def to_internal_value(self, data):
        print(data)
        return super(ObservableValueSerializer,self).to_internal_value(data)

    @transaction.atomic
    def update(self, instance, validated_data):
        pk = instance.id
        object = models.ObservableValue.objects.filter(id=pk)
        for key, value in validated_data.items():

            if key is "ip" and value:
                ipv = models.IpValue.objects.get_or_create(value=value)
                object.update(ip=ipv[0].id)

            if key is "email" and value:
                emailv = models.EmailValue.objects.get_or_create(value=value)
                object.update(email=emailv[0].id)

            if key is "string" and value:
                stringv = models.StringValue.objects.get_or_create(value=value)
                object.update(string=stringv[0].id)


        print(validated_data)
        instance.refresh_from_db()
        return instance

    @transaction.atomic
    def create(self, validated_data):
        print(self.object)
#        value = .objects.create(**validated_data)
#        if "members" in self.initial_data:
#            members = self.initial_data.get("members")
#            for member in members:
#                id = member.get("id")
#                role = member.get("role")
#                member_instance = Member.objects.get(pk=id)
#                GroupMember(group=group, member=member_instance, role=role).save()
#        group.save()
#        return project

def get_values(class_object):
    for item in class_object:
        print(item)

class ObservableSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="observables:observable-detail",
                    )

    id = serializers.ReadOnlyField()
    values_set = ObservableValueSerializer(source="values", many=True, read_only=False)
    class Meta:
        model = models.Observable
        fields = ('__all__')

    @transaction.atomic
    def update(self, instance, validated_data):
        # Ignore the fact that i delete and replace. Will diff in the future
        print(validated_data)

        pk = instance.id
        update = dict()
        for key, value in validated_data.items():
            if not key == "values":
                print(value)
                update[key] = value
        object = models.Observable.objects.filter(id=pk).update(**update)
        print(object)
        instance.refresh_from_db()
        return instance

