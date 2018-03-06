from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from users.models import Account
from . import models
from django.db.models import Q

class MotiveSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="common:motive-detail",
                    )
    name = serializers.CharField()

    class Meta:
        model = models.Motive
        fields = ('__all__')

    def update(self, instance, validated_data):
        if not "name" in validated_data:
            raise serializers.ValidationError("a motive needs a name")
        else:
            object, create = self.Meta().model.objects.update_or_create(
                name=validated_data["name"],
                defaults=validated_data )
            if not isinstance(instance, self.Meta().model):
                object.event.add(instance)
            return object

    def create(self, validated_data):
        if not "name" in validated_data:
            raise serializers.ValidationError("a motive needs a name")
        else:
            object = self.Meta().model.objects.get_or_create(
                name=validated_data["name"],
                defaults=validated_data)
            return object
        

class SectorClassField(serializers.PrimaryKeyRelatedField):

    def to_representation(self, instance):
        ret = super(SectorClassField, self).to_representation(instance)
        ret = (self.queryset.filter(id=ret).get().name)
        return ret

    def to_internal_value(self, value):
        try:
            ret = self.queryset.get(name=value)
        except:
            ret = self.queryset.get(id=value)
        return ret

class SectorClassSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField()

    class Meta:
        model = models.SectorClass
        fields = ('__all__')

    def create(self, validated_data):

        ModelClass = self.Meta.model

        # Remove many-to-many relationships from validated_data.
        # They are not valid arguments to the default `.create()` method,
        # as they require that the instance has already been saved.
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            instance = ModelClass.objects.get_or_create(**validated_data)
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                'exception was:\n %s' %
                (
                    ModelClass.__name__,
                    ModelClass.__name__,
                    self.__class__.__name__,
                    tb
                )
            )
            raise TypeError(msg)

        # Save many-to-many relationships after the instance is created.
        if many_to_many:
            for field_name, value in many_to_many.items():
                field = getattr(instance, field_name)
                field.set(value)

        return instance

    def update(self, instance, validated_data):
        if not "name" in validated_data:
            raise serializers.ValidationError("a sector needs a name")
        else:
            object, create = self.Meta().model.objects.update_or_create(
                name=validated_data["name"],
                defaults=validated_data )
            if not isinstance(instance, self.Meta().model):
                object.sector.add(instance)
            return object

    def create(self, validated_data):
        if not "name" in validated_data:
            raise serializers.ValidationError("a sector needs a name")
        else:
            object = self.Meta().model.objects.get_or_create(
                name=validated_data["name"],
                defaults=validated_data)
            return object


class MinSectorClassSerializer(SectorClassSerializer):

    def validate_empty_values(self, data):
        data = {"name": data}
        return (False, data)

    def to_representation(self, instance):
        ret = super(MinSectorClassSerializer, self).to_representation(instance)
        return ret["name"]
    
    def to_internal_value(self, instance):
        ret = super(MinSectorClassSerializer, self).to_internal_value(instance)
        return ret


class SectorSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="common:sector-detail",
                    )

    author = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField()
    sector_class = MinSectorClassSerializer(many=True)

    class Meta:
        model = models.Sector
        fields = ('__all__')

    def to_internal_value(self, instance):
        ret = super(SectorSerializer, self).to_internal_value(instance)
        return ret

    def update(self, instance, validated_data):
        info = model_meta.get_field_info(instance)

        remove = set()
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                for item in value:
                    serializer = SectorClassSerializer(instance, data=item)
                    if serializer.is_valid():
                       remove.add(serializer.save())
            else:
                setattr(instance, attr, value)
        # remove Observable
        initial_obs = instance.sector_class.all()
        old_obs = set([item for item in initial_obs])
        rm_old = old_obs.difference(remove)
        for item in rm_old:
            item.delete()
        instance.save()

        return instance



class SubjectSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                    view_name="common:subject-detail",
                    )

    class Meta:
        model = models.Subject
        fields = ('__all__')
