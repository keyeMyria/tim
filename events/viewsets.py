from . import models
from . import serializers
from actors.models import Actor
from rest_framework import viewsets
from users.views import UserCanViewDataMixin

class EventViewSet(UserCanViewDataMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows events to be added, viewed or edited.
    """
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer

class TypeViewSet(UserCanViewDataMixin, viewsets.ModelViewSet):
    queryset = models.Type.objects.all()
    serializer_class = serializers.TypeSerializer

class EventDocumentViewSet(UserCanViewDataMixin, viewsets.ModelViewSet):
    queryset = models.EventDocument.objects.all()
    serializer_class = serializers.EventDocumentSerializer

class EventObservablesViewSet(UserCanViewDataMixin, viewsets.ModelViewSet):
    queryset = models.EventObservable.objects.all()
    serializer_class = serializers.EventObservablesSerializer

class ActorViewSet(UserCanViewDataMixin, viewsets.ModelViewSet):
     queryset = Actor.objects.all()
     serializer_class = serializers.ActorSerializer

