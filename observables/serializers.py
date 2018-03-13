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
        values = self.Meta().model.objects.filter(
                **validated_data
                )
        obj = self.Meta().model.objects.filter(id=instance.id)
        if len(values) == 1:
            validated_data.pop("value")
        obj.update(**validated_data)

        instance.refresh_from_db()
        if isinstance(instance, self.Meta.model):
            return instance
        else:
            return obj

    @transaction.atomic
    def create(self, validated_data):
        values, create = self.Meta().model.objects.get_or_create(
                value=validated_data["value"])
        if create:
            do_also = self.Meta().model.objects.filter(id=values.id)
            do_also.update(**validated_data)

        values.refresh_from_db()
        return values

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

    @transaction.atomic
    def create(self, validated_data):
        values, create = self.Meta().model.objects.get_or_create(
                value=validated_data["value"])
        if create:
            do_also = self.Meta().model.objects.filter(id=values.id)
            do_also.update(**validated_data)

        values.refresh_from_db()
        return values

    def update(self, instance, validated_data):
        values = self.Meta().model.objects.filter(value = validated_data["value"])
        obj = self.Meta().model.objects.filter(id=instance.id)
        if len(values) == 1:
            validated_data.pop("value")
        obj.update(**validated_data)

        instance.refresh_from_db()
        if isinstance(instance, self.Meta.model):
            return instance
        else:
            return obj


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
        values = self.Meta().model.objects.filter(
                value = validated_data["value"])
        obj = self.Meta().model.objects.filter(id=instance.id)
        if len(values) == 1:
            validated_data.pop("value")
        obj.update(**validated_data)

        instance.refresh_from_db()
        if isinstance(instance, self.Meta.model):
            return instance
        else:
            return obj


    @transaction.atomic
    def create(self, validated_data):
        values, create = self.Meta().model.objects.get_or_create(
                value=validated_data["value"]
                )
        if create:
            do_also = self.Meta().model.objects.filter(id=values.id)
            do_also.update(**validated_data)

        values.refresh_from_db()
        return values


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

    @transaction.atomic
    def create(self, validated_data):
        values, create = self.Meta().model.objects.get_or_create(
                **validated_data)
        return values

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


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
        info = model_meta.get_field_info(instance)

        # update all values
        for attr, value in validated_data.items():
            # Deal with related fields
            if attr in info.relations and attr in self.select_serializer() and value:
                RelatedModel = info.relations[attr].related_model
                object = RelatedModel.objects.get(values=instance.id)
                new = set()
                serializer = self.select_serializer()[attr](object, data=value)
                if serializer.is_valid():
                    new.add(serializer.save())
                else:
                    print(serializer.errors)

            else:
                pass

        instance.save()
        return instance


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
        print("ret is %s" % ret)
        return ret


    def update(self, instance, validated_data):
        try:
            event = Event.objects.get(title=validated_data["event"])
            object, create = self.Meta.model.objects.get_or_create(
                event=event, observable=instance)
            return object
        except Exception as error:
            raise serializers.ValidationError("%s" % error)


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

        if "values" in attrs:
            if attrs["values"]:
                old_values = (attrs["values"][0]["observable"].values.values())
                new_values = attrs["values"]

                if len(attrs["values"]) == 2:
                    if attrs["values"][0]["type"] == attrs["values"][-1]["type"]:
                        raise serializers.ValidationError(
                                'Observables values with same type is not allowed')
        return attrs

    def get_serializer(self):
        serializers = {
            "event": EventObservablesSerializer,
            "values": ObservableValueSerializer,
        }
        return serializers

    def get_field(self, instance):
        # don't add through tables
        fields = {
        }

        return fields


    def update(self, instance, validated_data):
        print(validated_data)
        info = model_meta.get_field_info(instance)

        # update all values
        for attr, value in validated_data.items():
            # Deal with related fields
            if attr in info.relations and info.relations[attr].to_many:
                RelatedModel = info.relations[attr].related_model
                object = RelatedModel.objects.get(values=instance.id)
                old = set(RelatedModel.objects.filter(observable=instance.id))
                new = set()
                for item in value:
                    serializer = self.get_serializer()[attr](object, data=item)
                    if serializer.is_valid():
                        new.add(serializer.save())
                    else:
                        print(serializer.errors)

                print("new %s " %new)
                #if isinstance(instance, self.Meta.model):
                #    rm = old.difference(new)
                #    get_field = self.get_field(instance)
                #    for item in rm:
                #        # special case since observable is a through table
                #        if not attr in get_field:
                #            item.delete()
                #        else:
                #            get_field[attr].remove(item)

                #    add = new.difference(old)
                #    for item in add:
                #        # special case since observable is a through table
                #        if attr in get_field:
                #            item.event.add(instance)

            else:
                # set values to self
                setattr(instance, attr, value)

        instance.save()
        return instance
