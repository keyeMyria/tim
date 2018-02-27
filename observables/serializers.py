from rest_framework import serializers

from . import models
from events.models import Event
from django.db import transaction

class ObservableValueSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="observables:observable-value-detail",
                    )

    observable = serializers.PrimaryKeyRelatedField(many=False, queryset=models.Observable.objects.all())
    ip = serializers.StringRelatedField(many=False)
    email = serializers.StringRelatedField(many=False)
    string = serializers.StringRelatedField(many=False)
    type = serializers.StringRelatedField(many=False)
    id = serializers.ReadOnlyField()
    class Meta:
        model = models.ObservableValue
        fields = ('__all__')

#    @transaction.atomic
#    def update(self, instance, validated_data):
#        # Ignore the fact that i delete and replace. Will diff in the future
#        self.object.filter(group=instance).delete()
#        members = self.initial_data.get("members")
#        for member in members:
#            id = member.get("id")
#            role = member.get("role")
#            new_member = Member.objects.get(pk=id)
#            GroupMember(group=instance, member=new_member, role=role).save()
#
#        instance.__dict__.update(**validated_data)
#        instance.save()
#        return instance

    @transaction.atomic
    def create(self, validated_data):
        print(self.object)
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

    id = serializers.ReadOnlyField()
    values = ObservableValueSerializer(many=True, read_only=False)
    class Meta:
        model = models.Observable
        fields = ('__all__')
