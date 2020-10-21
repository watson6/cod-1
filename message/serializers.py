from rest_framework.serializers import ModelSerializer

from message.models import Message


class RestAPIMessageListSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'project', 'type', 'host', 'title', 'level', 'status', 'time']


class RestAPIMessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class RestAPICreateMessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
