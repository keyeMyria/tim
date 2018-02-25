from rest_framework import serializers

from . import models

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


class EventSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="events:event-detail",
                    )

    type = serializers.HyperlinkedRelatedField(
                    read_only=True,
                    view_name='events:type-detail',
                    )
    class Meta:
        model = models.Event
        fields = ('__all__')

