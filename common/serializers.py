from rest_framework import serializers

from . import models

class MotiveSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="common:motive-detail",
                    )

    class Meta:
        model = models.Motive
        fields = ('__all__')


class SectorSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="common:sector-detail",
                    )

    class Meta:
        model = models.Sector
        fields = ('__all__')

class SubjectSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="common:subject-detail",
                    )

    class Meta:
        model = models.Subject
        fields = ('__all__')
