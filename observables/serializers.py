from rest_framework import serializers

from . import models

class ObservableSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="observables:observable-detail",
                    )

    class Meta:
        model = models.Observable
        fields = ('__all__')

