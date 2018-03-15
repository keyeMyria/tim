from rest_framework import serializers, fields

from . import models
from events.models import EventObservable, Event
from django.db import transaction

import traceback
from rest_framework.utils import model_meta
from django.core.validators import validate_email, validate_ipv46_address
from django.urls import reverse_lazy
from rest_framework.utils import model_meta

def get_validator():
    validators = {
        "email": validate_email,
        "ip": validate_ipv46_address
    }
    return validators

def get_object():
    objects = {
        "email": models.EmailValue,
        "ip": models.IpValue,
        "string": models.StringValue
    }
    return objects


class IpValuesSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="observables:ip-value-detail",
                    )

    id = serializers.ReadOnlyField()
    type = "ip"

    value = serializers.IPAddressField(protocol='both')
    class Meta:
        model = models.IpValue
        fields = ('url','id', 'value', 'rateing', 'to_ids')


    def validate(self, attrs):
        value = attrs["value"]
        try:
            get_validator()[self.type](value)
        except Exception as e:
           raise serializers.ValidationError(e)
        return attrs


    def to_representation(self, instance):
        ret = super(IpValuesSerializer, self).to_representation(instance)
        ret.pop("id")
        return ret

    def to_internal_value(self, instance):
        ret = super(IpValuesSerializer, self).to_internal_value(instance)

        return ret

    def update(self, instance, validated_data):
        identify = validated_data.pop("value")
        object, created = self.Meta.model.objects.update_or_create(
            value=identify, defaults=(validated_data))
        return object

    @transaction.atomic
    def create(self, validated_data):
        identify = validated_data.pop("value")
        object, created = self.Meta.model.objects.update_or_create(
            value=identify, defaults=(validated_data))
        return object


class EmailValuesSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="observables:email-value-detail",
                    )

    value = serializers.EmailField()
    id = serializers.ReadOnlyField()
    type = "email"

    class Meta:
        model = models.EmailValue
        fields = ('url','id', 'value', 'rateing', 'to_ids')


    def validate(self, attrs):
        value = attrs["value"]
        try:
            get_validator()[self.type](value)
        except Exception as e:
           raise serializers.ValidationError(e)
        return attrs

    def to_representation(self, instance):
        ret = super(EmailValuesSerializer, self).to_representation(instance)
        ret.pop("id")
        return ret

    def to_internal_value(self, instance):
        ret = super(EmailValuesSerializer, self).to_internal_value(instance)
        return ret

    def create(self, validated_data):
        identify = validated_data.pop("value")
        object, created = self.Meta.model.objects.update_or_create(
            value=identify, defaults=(validated_data))
        return object

    def update(self, instance, validated_data):
        identify = validated_data.pop("value")
        object, created = self.Meta.model.objects.update_or_create(
            value=identify, defaults=(validated_data))
        return object

class StringValuesSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="observables:string-value-detail",
                    )

    id = serializers.ReadOnlyField()
    type = "string"
    value = serializers.CharField()

    class Meta:
        model = models.StringValue
        fields = ('url','id', 'value', 'rateing', 'to_ids')


    def validate(self, attrs):
        return attrs

    def to_representation(self, instance):
        ret = super(StringValuesSerializer, self).to_representation(instance)
        ret.pop("id")
        return ret

    def to_internal_value(self, instance):
        ret = super(StringValuesSerializer, self).to_internal_value(instance)
        return ret

    def update(self, instance, validated_data):
        identify = validated_data.pop("value")
        object, created = self.Meta.model.objects.update_or_create(
            value=identify, defaults=(validated_data))
        return object

    def create(self, validated_data):
        identify = validated_data.pop("value")
        object, created = self.Meta.model.objects.update_or_create(
            value=identify, defaults=(validated_data))
        return object


class FileValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FileValue
        fields = ('__all__')


class ObservableTypeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    url = serializers.HyperlinkedIdentityField(
                    view_name="observables:observable-type-detail",
                    )

    class Meta:
        model = models.ObservableType
        fields = ('__all__')

    def validate(self, attrs):
        return attrs

    def to_representation(self, instance):
        ret = super(ObservableTypeSerializer, self).to_representation(instance)
        return ret

    def to_internal_value(self, instance):
        ret = super(ObservableTypeSerializer, self).to_internal_value(instance)
        return ret

    def create(self, validated_data):
        identify_by = validated_data.pop("name")
        object, created = self.Meta.model.objects.update_or_create(
            name=identify_by, defaults=validated_data
        )
        return object

    def update(self, instance, validated_data):
        identify_by = validated_data.pop("name")
        object, created = self.Meta.model.objects.update_or_create(
            name=identify_by, defaults=validated_data
        )

        return object


class ObservableValueSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="observables:observable-value-detail",
                    )


    observable = serializers.SlugRelatedField(
            read_only=False,
            many=False,
            queryset=models.Observable.objects.all(),
            slug_field='name'
            )


    ip = IpValuesSerializer(required=False, allow_null=True)
    email = EmailValuesSerializer(required=False, allow_null=True)
    string = StringValuesSerializer(required=False, allow_null=True)
    type = ObservableTypeSerializer(required=True)
    skip_fields = list()
    id = serializers.ReadOnlyField()

    class Meta:
        model = models.ObservableValue
        fields = ('__all__')

    def select_serializer(self):
        serializer = {
            "ip": IpValuesSerializer,
            "email": EmailValuesSerializer,
            "string": StringValuesSerializer,
            "type": ObservableTypeSerializer 
        }
        return serializer

    def select_model(self):
        models = {
            "ip": models.IpValue,
            "email": models.EmailValue,
            "string": models.StringValue
        }

    def get_orig_value(self, instance):
        value = {
            "ip": instance.ip,
            "email": instance.email,
            "string": instance.string
        }
        return value

    def update(self, instance, validated_data):
        info = model_meta.get_field_info(self.Meta.model)
        observable = validated_data.pop("observable")
        # update all values
        
        self_filter = {"observable": observable}

        for attr, value in validated_data.items():
            # Deal with related fields
            if value and attr in self.select_serializer():
                RelatedModel = info.relations[attr].related_model
                related_id = None
                serializer = self.select_serializer()[attr](instance, data=value)
                if serializer.is_valid():
                    obj = serializer.save()
                    self_filter[attr] = obj
                else:
                    print(serializer.errors)

        object, created = self.Meta.model.objects.update_or_create(**self_filter)
        return object



class EventField(serializers.Field):

    def to_representation(self, obj):
        return obj.title

    def to_internal_value(self, data):
        return data.strip(' ')


class EventObservablesSerializer(serializers.ModelSerializer):

    observable = serializers.SlugRelatedField(
            read_only=True,
            many=False,
            slug_field='name',
            required = False
            )

    event = EventField()

    id = serializers.ReadOnlyField()
    obs = None

    def validate_empty_values(self, data):
        if isinstance(data, str):
            data = {"event" : data}
        return (False, data)

    def validate(self, attrs):
        return attrs

    class Meta:
        model = EventObservable
        fields = ('__all__')

    def to_representation(self, instance):
        ret = super(EventObservablesSerializer, self).to_representation(instance)
        return ret["event"]

    def to_internal_value(self, instance):
        ret = super(EventObservablesSerializer, self).to_internal_value(instance)
        return ret


    def update(self, instance, validated_data):
        info = model_meta.get_field_info(self.Meta.model)
        RelatedModel = info.relations["event"].related_model
        event = RelatedModel.objects.get(title=validated_data["event"])
        
        object, created = self.Meta.model.objects.get_or_create(
            event=event, observable=instance
        )
        return object

    def create(self, validated_data):
        return None

class ObservableSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="observables:observable-detail",
                    )


    event = EventObservablesSerializer(many=True, read_only=False)
    id = serializers.ReadOnlyField()
    values = ObservableValueSerializer(many=True, read_only=False)


    class Meta:
        model = models.Observable
        fields = ('__all__')

    def validate(self, attrs):
        return attrs

    def get_serializer(self):
        serializers = {
            "event": EventObservablesSerializer,
            "values": ObservableValueSerializer,
        }
        return serializers


    def update(self, instance, validated_data):
        if not isinstance(instance, self.Meta.model):
            raise serializers.ValidationError(
               'instance has to be Observable')
       
        info = model_meta.get_field_info(instance)

        # update all values
        for attr, value in validated_data.items():
            # Deal with related fields
            new = set()
            if attr in self.get_serializer():
                RelatedModel = info.relations[attr].related_model
                qs = RelatedModel.objects.filter(observable=instance)
                for item in value:
                    item["observable"] = instance
                    serializer = self.get_serializer()[attr](instance, data=item)
                    if serializer.is_valid():
                        new.add(serializer.save())
                    else:
                        print(serializer.errors)

                old = set([item for item in qs])
                rm = old.difference(new)
                for item in rm:
                    item.delete()

            else:
                # set values to self
                setattr(instance, attr, value)


        instance.save()
        return instance
