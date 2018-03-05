from rest_framework import serializers, fields

from . import models
from events.models import EventObservable, Event
from django.db import transaction

import traceback
from rest_framework.utils import model_meta
from django.core.validators import validate_email, validate_ipv46_address
from django.urls import reverse_lazy

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
        return instance

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
        return instance


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
        return instance

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
        values = self.Meta().model.objects.filter(
                value = validated_data["value"]
                )
        obj = self.Meta().model.objects.filter(id=instance.id)
        if len(values) == 1:
            validated_data.pop("value")
        obj.update(**validated_data)

        instance.refresh_from_db()
        return instance


class ObservableValueSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="observables:observable-value-detail",
                    )

    observable = serializers.PrimaryKeyRelatedField(
            many=False,
            queryset=models.Observable.objects.all()
            )

    ip = IpValuesSerializer(required=False, allow_null=True)
    email = EmailValuesSerializer(required=False, allow_null=True)
    string = StringValuesSerializer(required=False, allow_null=True)
    type = ObservableTypeSerializer(required=True)
    skip_fields = list()
    id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = models.ObservableValue
        fields = ('__all__')
        extra_kwargs = {'id': {'read_only': False}}

    def to_internal_value(self, instance):
        ret = super(ObservableValueSerializer, self).to_internal_value(instance)
        return ret

    def validate_empty_values(self, data):
        ret = data.copy()
        for item, value in data.items():
            if value is None:
                self.skip_fields.append(item)
                ret.pop(item)
        return (False, data)

    def validate(self, attrs):
        if "id" in attrs:
            ObsVal = models.ObservableValue.objects.get(id=attrs["id"])
            if ObsVal.observable_id:
                if not int(ObsVal.observable_id) == int(attrs["observable"].id):
                    raise serializers.ValidationError(
                            "This value is used by: %s"%
                            models.Observable.objects.get(id=int(ObsVal.observable_id)))

        if ("type" and "observable" in attrs):
            valid = dict()

            if len(attrs["observable"].values.values()) > 1:
                raise serializers.ValidationError(
                        "maximum observable values is 2")
                

            # validate observable
            if "observable" in attrs:
                valid["observable"] = attrs["observable"]
                attrs.pop("observable", None)

            for key, value in attrs.items():
                valid[key] = None

                if value:
                    if str(value) == "NULL":
                        valid[key] = "NULL"

                valid[key] = value

                if str(value) == "NULL":
                    continue

                if not key in attrs["type"]["type_class"] and value:
                    if not key == "id":
                        raise serializers.ValidationError(
                                '%s field must be empty with type: %s' 
                                % (key, attrs["type"]["type_class"]))

            return valid
        else:
            return attrs



    def select_serializer(self):
        serializer = {
            "ip": IpValuesSerializer,
            "email": EmailValuesSerializer,
            "string": StringValuesSerializer
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

    @transaction.atomic
    def update(self, instance, validated_data):
        pk = instance.id
        object = models.ObservableValue.objects.filter(id=pk)
        serializer = self.select_serializer()
        for key, value in validated_data.items():
            if key in serializer and value:
                svalue = serializer[key](data=value)
                if not svalue.is_valid():
                    print(serializer.errors)
                else:
                    new = svalue.save()
                    svalue.update(new, svalue.validated_data)
                    new.obs_values.add(instance)
                    continue
            elif value:
                if "observable" in key and not isinstance(value, int):
                    value.values.add(instance)

        instance.refresh_from_db()
        return instance

    def get_serializer(self):
        serializers = {
                "ip":IpValuesSerializer,
                "email":EmailValuesSerializer,
                "string":StringValuesSerializer
                }

        return serializers

    @transaction.atomic
    def create(self, validated_data):
        print("Createing ObservableValues")
        obj = None
        values = None
        type = None
        send = dict()
        observable = validated_data.pop("observable")
        type = validated_data.pop("type")

        type_serial = ObservableTypeSerializer(data=type)
        if type_serial.is_valid():
            type = type_serial.save()
            send["type"] = type
        else:
            raise serializers.ValidationError(type.errors)

        for key, value in validated_data.items():

            if key in self.get_serializer() and value:
                values_serial = self.get_serializer()[key](data=value)
                if values_serial.is_valid():
                    values = values_serial.save()
                    send[key] = values
                else:
                    raise serializers.ValidationError(values.errors)

        send["observable"] = observable
        values, created = self.Meta().model.objects.update_or_create(**send)
        return values


class ObservableSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="observables:observable-detail",
                    )


    event = serializers.PrimaryKeyRelatedField(many=True, queryset=Event.objects.all())
    id = serializers.ReadOnlyField()
    values = ObservableValueSerializer(many=True, read_only=False)

    class Meta:
        model = models.Observable
        fields = ('__all__')

    def to_internal_value(self, data):
        to_internal = super(ObservableSerializer,self).to_internal_value(data)
        return to_internal


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


    @transaction.atomic
    def update(self, instance, validated_data):
        pk = instance.id
        clean_values = validated_data.pop("values")
        old_values = models.Observable.objects.get(pk=pk).values.all()
        new_values = list()
        obsvalues = instance.values.all()
        

        for index, item in enumerate(clean_values):
            item["observable"] = pk

            if "id" in item:
                ObsVal = models.ObservableValue.objects.get(pk=item["id"])
                values = ObservableValueSerializer(ObsVal, data=item)
            else:
                values = ObservableValueSerializer(data=item)

            if not values.is_valid():
                raise serializers.ValidationError(
                        "%s" % values.errors)

            else:
                values = values.save()
                new_values.append(values)

        object = models.Observable.objects.filter(id=pk)
        object.update(**validated_data)

        if not clean_values:
            for item in object.get().values.all():
                instance.values.remove(item)

        old = set([item for item in old_values])
        new = set([item for item in new_values])
        rm = new.symmetric_difference(old)
        if rm:
            for item in rm:
               instance.values.remove(item)
               item.delete()



        instance.refresh_from_db()
        return instance

