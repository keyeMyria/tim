from rest_framework import serializers
from . import models
from common.serializers import MotiveSerializer, SectorSerializer
from observables.serializers import ObservableSerializer

from django_countries.serializers import CountryFieldMixin
from django_countries.serializer_fields import CountryField
from observables.models import Observable

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

class EventObservablesSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="events:event-observable-detail",
                    )


    observable = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Observable.objects.all())
    event = serializers.PrimaryKeyRelatedField(read_only=False, queryset=models.Event.objects.all())

    class Meta:
        model = models.EventObservable
        fields = ('__all__')


class EventSerializer(CountryFieldMixin, serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="events:event-detail",
                    )

#    type = serializers.HyperlinkedRelatedField(
#                    read_only=True,
#                    view_name='events:type-detail',
#                    )
#
#    observables = EventObservablesSerializer()
#    motive = MotiveSerializer(many=True) 
#    motive = serializers.StringRelatedField(many=True)
    #sector = MotiveSerializer(many=True) 
#    sector = serializers.StringRelatedField(many=True)
#    observable = EventObservablesSerializer(many=True)
    observable = serializers.PrimaryKeyRelatedField(many=True, queryset=models.EventObservable.objects.all())
#    observable = serializers.StringRelatedField(many=True)
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()

    class Meta:
        country_dict=True
        model = models.Event
#        fields = ('__all__')
        exclude = ("motive", "sector")

