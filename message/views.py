from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from utils.drf.mixins import MultiSerializersMixin
from message.models import Message
from message.serializers import MessageListSerializer, MessageRetrieveSerializer
from data_source.authentications import TokenAuthentication


class MessageViewSets(MultiSerializersMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Message.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    serializer_class_mapping = {
        'list': MessageListSerializer,
        'retrieve': MessageRetrieveSerializer
    }
    search_fields = ['project', 'type', 'host', 'title', 'desc']
    authentication_classes = [TokenAuthentication]
