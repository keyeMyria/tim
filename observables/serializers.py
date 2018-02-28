from rest_framework import serializers, fields

from . import models
from events.models import EventObservable, Event
from django.db import transaction

import traceback
from rest_framework.utils import model_meta
from django.core.validators import validate_email, validate_ipv46_address

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

#    def to_representation(self, data):
#        print(data)

    def validate_empty_values(self, data):
        return (True, data)


def get_validator():
    validators = {
        "email": validate_email,
        "ip": validate_ipv46_address
    }
    return validators

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
    own_id = None

    def validate(self, attrs):
        if "type" and "observable" in attrs: 
            type = models.ObservableValue.objects.get(id=self.own_id).type
            type_class = type.type_class
            valid = dict()
            valid["observable"] = attrs["observable"]
            attrs.pop("observable", None)
            valid["id"] = self.own_id

            if not str(type) in attrs["type"]:
               raise serializers.ValidationError('type change is not allowed')

            valid["type"] = str(type)
            attrs.pop("type", None)

            for key, value in attrs.items():
                valid[key] = None

                if value:
                    if str(value) == "NULL":
                        valid[key] = "NULL"

                if key in type_class:
                    valid[key] = value
                    try:
                         get_validator()[key](value)
                    except Exception as e:
                        raise serializers.ValidationError('%s' % (e))


                if str(value) == "NULL":
                    continue
                if not key in type_class and value:
                    raise serializers.ValidationError('%s field must be empty with type: %s' % (key, type_class))

            return valid
        else:
            return attrs

    class Meta:
        model = models.ObservableValue
        fields = ('__all__')

    def to_internal_value(self, data):
        try:
            self.own_id = data["id"]
        except:
            self.own_id = None
        return super(ObservableValueSerializer,self).to_internal_value(data)

    @transaction.atomic
    def update(self, instance, validated_data):
        pk = instance.id
        object = models.ObservableValue.objects.filter(id=pk)
        for key, value in validated_data.items():

            if key is "ip" and value:
                if value == "NULL":
                    instance.ip.delete()
                else:
                    ipv = models.IpValue.objects.get_or_create(value=value)
                    object.update(ip=ipv[0].id)

            if key is "email" and value:
                if value == "NULL":
                    instance.email.delete()
                else:
                    emailv = models.EmailValue.objects.get_or_create(value=value)
                    object.update(email=emailv[0].id)

            if key is "string" and value:
                print(key)
                stringv = models.StringValue.objects.get_or_create(value=value)
                if value == "NULL":
                    instance.string.delete()
                else:
                    stringv = models.StringValue.objects.get_or_create(value=value)
                    object.update(string=stringv[0].id)


        instance.refresh_from_db()
        return instance

    @transaction.atomic
    def create(self, validated_data):
        print(validated_data)
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


    event = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    id = serializers.ReadOnlyField()
    values = ObservableValueSerializer(many=True, read_only=False)
    value_ids = list()

    class Meta:
        model = models.Observable
        fields = ('__all__')

    def validate(self, attrs):
        return attrs

    def to_internal_value(self, data):
        
        self.value_ids = list()
        for item in data["values"]:
            item["id"]
            self.value_ids.append(item["id"])
        return super(ObservableSerializer,self).to_internal_value(data)

    @transaction.atomic
    def update(self, instance, validated_data):
        pk = instance.id
        update = dict()
        for key, value in validated_data.items():
            if not key == "values":
                update[key] = value
            else:
                for index, val_pk in enumerate(self.value_ids):
                    send = dict()
                    if value and "observable" in value[index]:
                        send = value[index]
                        send["observable"] = value[index]["observable"].id
                        value_filter = models.ObservableValue.objects.filter(pk=val_pk)
                        if value_filter.values():
                            value_instance = value_filter.get()
                            serializer = ObservableValueSerializer(data=send)
                            if not serializer.is_valid():
                                print(serializer.errors)
                            else:
                                print(serializer.validated_data)
                                serializer.update(instance=value_instance, validated_data=send)

        excisting = instance.values.all()
        orig_val = list()

        for item in excisting.values():
            orig_val.append(item["id"])

        if orig_val:
            for item in orig_val:
                if item in self.value_ids:
                    continue
                else:
                    rem = instance.values.get(id=item)
                    instance.values.remove(rem)

        for item in self.value_ids:
            if not item in excisting.values():
                try:
                    new = models.ObservableValue.objects.get(id=item)
                except:
                    continue
                instance.values.add(new)

        object = models.Observable.objects.filter(id=pk).update(**update)
        instance.refresh_from_db()
        return instance

