from rest_framework import serializers
from . import models
from common.serializers import MotiveSerializer, SectorSerializer
from observables.serializers import ObservableSerializer
from django.db.models import Manager
from django.db.models.query import QuerySet


from django_countries.serializers import CountryFieldMixin
from django_countries.serializer_fields import CountryField
from observables.models import Observable
from common.serializers import MotiveSerializer, SectorSerializer
from django.utils.translation import ugettext_lazy as _
from django.db import transaction
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

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
        return ret


    def update(self, instance, validated_data):

        # add if not already excists
        object, created = self.Meta().model.objects.get_or_create(
            observable=validated_data["observable"],
            event=instance
        )

        return object

    @transaction.atomic
    def create(self, validated_data):
        return None

class MinSectorSerializer(SectorSerializer):

    def to_representation(self, instance):
        ret = super(MinSectorSerializer, self).to_representation(instance)
        return ret["name"]

    def to_internal_value(self, instance):
        ret = super(MinSectorSerializer, self).to_internal_value(instance)
        print(ret)        
        return ret

    def validate_empty_values(self, data):
        print(data)
        return (False, data)


class EventSerializer(CountryFieldMixin, serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="events:event-detail",
                    )

    observable = EventObservablesSerializer(many=True)
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()
    motive = MotiveSerializer(many=True)
    sector = MinSectorSerializer(many=True)

    class Meta:
        country_dict=True
        model = models.Event
#        fields = ('__all__')
        exclude = ("targeted_organization", "reporter")
        validators = []

    def validate_empty_values(self, data):
        print(data)
        return (False, data)


    def to_internal_value(self, instance):
        ret = super(EventSerializer, self).to_internal_value(instance)
        print(ret)
        return ret

    def get_serializer(self):
        serializers = {
            "sector": SectorSerializer
        }
        return serializers

    def update(self, instance, validated_data):
        # Observable data
        obs_data = validated_data["observable"]
        motives = validated_data["motive"]
        sectors = validated_data["sector"]
        validated_data.pop("observable")
        validated_data.pop("motive")
        obs_qs = models.Observable.objects.all()
        obs_ev_qs = models.EventObservable.objects.all()



        new_mots = set()
        for motive in motives:
            motive = MotiveSerializer(instance, data=motive)
            if motive.is_valid():
                new_mots.add(motive.save())
            else:
                print(motive.errors)

        print(validated_data)
        new_obs = set()
        for obs in obs_data:
            #TODO: create a decent validator for when obs is missing
            if obs["observable"]:
                send = {"observable": obs["observable"].uuid} 
                obs_serial = EventObservablesSerializer(instance, data=send)
                if obs_serial.is_valid():
                    ob = obs_serial.save()
                    new_obs.add(ob)
                else:
                    print(obs_serial.errors)

        #raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        new_secs = set()
#        print(sectors)
#        print(info.relations)
#        for item in info.relations:
#            print(item)

        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                #field = getattr(instance, attr)
                for item in value:
                    serializer = self.get_serializer()[attr](instance, data=item)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        print(serializer.errors)
                #field.set(value)
                
            else:
                #print(value)
                setattr(instance, attr, value)

#        for sector in sectors:
#            
#            #sector = SectorSerializer(instance, data=sector)
#            if sector.is_valid():
#                new_secs.add(sector.save())
#            else:
#                print(sector.errors)


#        # remove Observable
#        initial_obs = instance.observable.all()
#        old_obs = set([item for item in initial_obs])
#        rm_old = old_obs.difference(new_obs)
#        for item in rm_old:
#            item.delete()
#
#        # remove motive
#        initial_motives = instance.motive.all()
#        old_mots = set([item for item in initial_motives])
#        rm_old = old_mots.difference(new_mots)
#        for item in rm_old:
#            instance.motive.remove(item)
#
#        # handle everything remaining
#        object = self.Meta().model.objects.filter(id=instance.id).update(**validated_data)
#        instance.refresh_from_db()
        instance.save()
        return instance

    @transaction.atomic
    def create(self, validated_data):
        print(validated_data)
        obs_data = validated_data["observable"]
        validated_data.pop("observable")
        instance = self.Meta().model.objects.create(**validated_data)

        new_obs = set()
        for obs in obs_data:
            #TODO: create a decent validator for when obs is missing
            if obs["observable"]:
                send = {"observable": obs["observable"].uuid}
                obs_serial = EventObservablesSerializer(instance, data=send)
                if obs_serial.is_valid():
                    ob = obs_serial.save()
                    new_obs.add(ob)
                else:
                    print(obs_serial.error)
        return instance

