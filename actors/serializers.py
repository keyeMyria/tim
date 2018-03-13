from rest_framework import serializers
from . import models

from django_countries.serializer_fields import CountryField
from django_countries.serializers import CountryFieldMixin

#from events.serializers import EventSerializer
from rest_framework.utils import model_meta


class ActorTypeSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="actors:actor-type-detail",
                    )

    class Meta:
        model = models.ActorType
        fields = ('__all__')


class TypeField(serializers.Field):

    def to_representation(self, obj):
        return obj.name

    def to_internal_value(self, data):
        return data.strip(' ')

class MinActorTypeSerializer(ActorTypeSerializer):

    name = serializers.CharField()

    class Meta:
        model = models.ActorType
        fields = ('__all__')

    def to_representation(self, instance):
        ret = super(MinActorTypeSerializer, self).to_representation(instance)
        return ret["name"]

    def to_internal_value(self, instance):
        ret = super(MinActorTypeSerializer, self).to_internal_value(instance)
        return ret

    # only allow selecting excisting
    def update(self, instance, validated_data):
        if not "name" in validated_data:
            raise serializers.ValidationError("an actor needs a name")
        else:
            try:
                object = self.Meta().model.objects.get(
                    name=validated_data["name"])
            except Exception as error:
                raise serializers.ValidationError(error)

            return object


class OrganizationDomainSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="actors:organization-domain-detail",
                    )

    class Meta:
        model = models.OrganizationDomain
        fields = ('__all__')


class OrganizationSerializer(CountryFieldMixin, serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="actors:organization-detail",
                    )

    type = TypeField()

    class Meta:
        country_dict=True
        model = models.Organization
        fields = ('__all__')

    def to_internal_value(self, instance):
        ret = super(OrganizationSerializer, self).to_internal_value(instance)
        return ret

    def to_representation(self, instance):
        ret = super(OrganizationSerializer, self).to_representation(instance)
        return ret

    def get_serializer(self):
        serializers = {
            "type": MinActorTypeSerializer,
        }
        return serializers

    def get_field(self, instance):
        # don't add through tables
        fields = {
            "type": instance.type,
        }

        return fields


    # only allow selecting excisting
    def update(self, instance, validated_data):
        print(validated_data)
        info = model_meta.get_field_info(instance)

        # update all values
        remove = []
        for attr, value in validated_data.items():
            # remove all many to many values for now
            # TODO: TTPs need implementation
            if attr in info.relations and info.relations[attr].to_many:
                RelatedModel = info.relations[attr].related_model
                remove.append(attr)

        for item in remove:
            validated_data.pop(item)

        for attr, value in validated_data.items():

            if attr in self.get_serializer() and not info.relations[attr].to_many:
                serial = self.get_serializer()[attr](instance, {"name": value})
                if serial.is_valid():
                    valid = serial.save()
                    setattr(instance, attr, valid)
                else:
                    raise serializers.ValidationError(serial.errors)
            else:
                setattr(instance, attr, value)

        instance.save()
        return instance

    def create(self, validated_data):
        # TODO: implement create
        raise serializers.ValidationError(
            "Creation of organizations is not implemented")
        



class MinOrganizationSerializer(OrganizationSerializer):
    name = serializers.CharField()

    def validate_empty_values(self, data):
        if isinstance(data, str):
            data = {"name": data}
        return (True, data)

    def to_representation(self, instance):
        ret = super(OrganizationSerializer, self).to_representation(instance)
        return ret["name"]

    def to_internal_value(self, instance):
        ret = super(OrganizationSerializer, self).to_internal_value(instance)
        return ret

    # only allow selecting excisting
    def update(self, instance, validated_data):
        if not "name" in validated_data:
            raise serializers.ValidationError("an event needs a name")
        else:
            try:
                object = self.Meta().model.objects.get(
                    name=validated_data["name"])
            except Exception as error:
                raise serializers.ValidationError(error)
            return object


#class EventField(serializers.Field):
#
#    def to_representation(self, obj):
#        return obj.title
#
#    def to_internal_value(self, data):
#        return data.strip(' ')
#
#
#class MinEventSerializer(EventSerializer):
#    title = serializers.CharField()
#
#    def validate_empty_values(self, data):
#        if isinstance(data, str):
#            data = {"title": data}
#        return (True, data)
#
#    def to_representation(self, instance):
#        ret = super(MinEventSerializer, self).to_representation(instance)
#        return ret["title"]
#
#    def to_internal_value(self, instance):
#        ret = super(MinEventSerializer, self).to_internal_value(instance)
#        return {"title": ret}
#
#    # only allow selecting excisting
#    def update(self, instance, validated_data):
#        if not "title" in validated_data:
#            raise serializers.ValidationError("an event needs a name")
#        else:
#            try:
#                object = self.Meta().model.objects.get(
#                    title=validated_data["title"])
#            except Exception as error:
#                raise serializers.ValidationError(error)
#            return object
#
#    def create(self, validated_data):
#        raise serializers.ValidationError(
#            "Creation of events is not permitted")
#
#
class ActorSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="actors:actor-detail",
                    )

    event = serializers.PrimaryKeyRelatedField(read_only=True)
    actor = MinOrganizationSerializer(many=True)
    class Meta:
        model = models.Actor
        fields = ('__all__')

    def to_internal_value(self, instance):
        ret = super(ActorSerializer, self).to_internal_value(instance)
        return ret

    def to_representation(self, instance):
        ret = super(ActorSerializer, self).to_representation(instance)
        return ret

    def get_serializer(self):
        serializers = {
            "actor": MinOrganizationSerializer,
            "event": MinEventSerializer,
        }
        return serializers

    def get_field(self, instance):
        # don't add through tables
        fields = {
            "actor": instance.actor,
        }
        return fields


    # only allow selecting excisting
    def update(self, instance, validated_data):
        info = model_meta.get_field_info(instance)

        # update all values
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                RelatedModel = info.relations[attr].related_model
                old = set(RelatedModel.objects.filter(actor=instance.id))
                new = set()
                for item in value:
                    serial = self.get_serializer()[attr](instance, item)
                    if serial.is_valid():
                        valid = serial.save()
                        new.add(valid)
                    else:
                        raise serializers.ValidationError("some error")

                if isinstance(instance, self.Meta.model):
                    rm = old.difference(new)
                    get_field = self.get_field(instance)
                    for item in rm:
                        # special case since observable is a through table
                        if not attr in get_field:
                            item.delete()
                        else:
                            # use remove or other end is deleted too w/ MtM
                            get_field[attr].remove(item)

                    add = new.difference(old)
                    for item in add:
                        get_field[attr].add(item)


            elif attr in self.get_serializer() and not info.relations[attr].to_many:
                serial = self.get_serializer()[attr](instance, value)
                if serial.is_valid():
                    valid = serial.save()
                    setattr(instance, attr, valid)
                else:
                    raise serializers.ValidationError("some error")

            else:
                setattr(instance, attr, value)

        instance.save()
        return instance
