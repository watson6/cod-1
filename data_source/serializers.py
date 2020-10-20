import json
from rest_framework.serializers import ModelSerializer
from message.models import Message
from utils.drf.decorators import validate_field_value
from utils.drf.serializers import RobustSerializer


class MessageListSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'project', 'type', 'host', 'title', 'level', 'status', 'time']


class MessageRetrieveSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class RestAPIMessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class PrometheusMessageSerializer(RobustSerializer):
    class Meta:
        model = Message
        fields = '__all__'

    @staticmethod
    @validate_field_value
    def get_project(field, data):
        """获取项目名称"""
        try:
            return '%s_%s' % (data['labels'].get("productline"), data['labels'].get("product"))
        except KeyError:
            return 'Prometheus'

    @staticmethod
    @validate_field_value
    def get_type(field, data):
        """获取告警标识"""
        return data['labels'].get("alertname", "")

    @staticmethod
    @validate_field_value
    def get_host(field, data):
        """获取告警主机"""
        return data['labels'].get("ipaddress", "")

    @staticmethod
    @validate_field_value
    def get_title(field, data):
        """获取告警标题"""
        return data['annotations'].get("summary", "")

    @staticmethod
    @validate_field_value
    def get_desc(field, data):
        """获取告警描述"""
        return data['annotations'].get("description", "")

    @staticmethod
    @validate_field_value
    def get_level(field, data):
        """获取告警等级"""
        level = data['labels'].get('severity', "")
        mapping = {"warning": 1, "critical": 2, "disaster": 3}
        return mapping[level]

    @staticmethod
    @validate_field_value
    def get_status(field, data):
        """获取告警状态"""
        status = data['status']
        mapping = {"firing": 0, "resolved": 1}
        return mapping[status]

    @staticmethod
    @validate_field_value
    def get_raw(field, data):
        """获取告警原始数据"""
        return json.dumps(data['labels'])

    @staticmethod
    @validate_field_value
    def get_tags(field, data):
        """获取告警标签"""
        return ""

    @staticmethod
    @validate_field_value
    def get_time(field, data):
        """获取告警时间"""
        return data['startsAt']


