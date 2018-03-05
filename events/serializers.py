from rest_framework import serializers
from . import models
from common.serializers import MotiveSerializer, SectorSerializer
from observables.serializers import ObservableSerializer
from django.db.models import Manager
from django.db.models.query import QuerySet


from django_countries.serializers import CountryFieldMixin
from django_countries.serializer_fields import CountryField
from observables.models import Observable
from django.utils.translation import ugettext_lazy as _
from django.db import transaction

class TypeSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="events:type-detail",
                    )

    event = serializers.HyperlinkedRelatedField(
                    many=True,
                    read_only=True,
                    view_name='events:event-detail',
                    )

    class Meta:
        model = models.Type
        fields = ('__all__')

class EventDocumentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="events:event-document-detail",
                    )

    event = serializers.HyperlinkedRelatedField(
                    many=False,
                    read_only=True,
                    view_name='events:event-detail',
                    )


    class Meta:
        model = models.EventDocument
        fields = ('__all__')

class ObservableField(serializers.Field):

    def to_representation(self, obj):
        return obj.uuid

    def to_internal_value(self, data):
        qs = Observable.objects.filter(uuid=data)
        if qs:
            return qs.get()
        else:
            serializers.ValidationError('This observable does not excist')


class EventObservablesSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="observables:observable-detail",
                    )


    observable = ObservableField()

    event = serializers.PrimaryKeyRelatedField(read_only=True)

    id = serializers.ReadOnlyField()
    obs = None

    def validate_empty_values(self, data):
        return (False, data)

    def validate(self, attrs):
        return attrs

    class Meta:
        model = models.EventObservable
        fields = ('__all__')

    def to_representation(self, instance):
        ret = super(EventObservablesSerializer, self).to_representation(instance)
        ret.pop("id")
        ret.pop("event")
        return ret

    def to_internal_value(self, instance):
        ret = super(EventObservablesSerializer, self).to_internal_value(instance)
        print("ret: %s" % ret)
        return ret


    def update(self, instance, validated_data):
        object = self.Meta().model.objects.filter(
            event=instance.id,
            observable=validated_data["observable"]).get()
        print(instance)
        print(object)
        print(validated_data)

        return object

    @transaction.atomic
    def create(self, validated_data):
        return None


class EventSerializer(CountryFieldMixin, serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="events:event-detail",
                    )

    observable = EventObservablesSerializer(many=True)
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()

    class Meta:
        country_dict=True
        model = models.Event
#        fields = ('__all__')
        exclude = ("motive", "sector")

    def to_internal_value(self, instance):
        ret = super(EventSerializer, self).to_internal_value(instance)
        return ret


    def update(self, instance, validated_data):
        # Observable data
        obs_data = validated_data["observable"]
        obs_qs = models.Observable.objects.all()
        obs_ev_qs = models.EventObservable.objects.all()
        print(obs_data)

        saved_obs = list()

        for obs in obs_data:
            #TODO: create a decent validator for when obs is missing
            if obs["observable"]:
                send = {"observable": obs["observable"].uuid} 
                obs_serial = EventObservablesSerializer(instance, data=send)
                if obs_serial.is_valid():
                    saved_obs.append(obs_serial.save())
                else:
                    print(obs_serial.errors)

        #print(saved_obs)
        #for item in saved_obs:
        #    print(item.id)

        #saved_obs = set([obs.id for obs in saved_obs]
        #new_obs = set([obs["observable"].id for obs in obs_data])
       # new = new_obs.difference(old_obs)
       # rm = old_obs.difference(new_obs)

        
        instance.refresh_from_db()
        return instance

    @transaction.atomic
    def create(self, validated_data):
        print(validated_data) 
        values.refresh_from_db()
        return values

