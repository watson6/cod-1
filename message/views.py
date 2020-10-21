from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from utils.drf.mixins import MultiSerializersMixin

from data_source.authentications import TokenAuthentication
from message.models import Message
from message.serializers import RestAPIMessageSerializer, RestAPICreateMessageSerializer


class RestAPIMessageViewSets(MultiSerializersMixin, CreateModelMixin, GenericViewSet):
    queryset = Message.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    serializer_classes = [RestAPICreateMessageSerializer]
    search_fields = ['project', 'type', 'host', 'title', 'desc']
    authentication_classes = [TokenAuthentication]
