from jsonpath_rw import parse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from data_source.authentications import RestFulAuthentication, PrometheusAuthentication
from data_source.serializers import RestFulMessageSerializer, PrometheusMessageSerializer
from message.models import Message


# Create your views here.

class RestFulMessageViewSets(CreateModelMixin, GenericViewSet):
    queryset = Message.objects.filter()
    serializer_class = RestFulMessageSerializer
    authentication_classes = [RestFulAuthentication]


class PrometheusMessageViewSets(CreateModelMixin, GenericViewSet):
    """ Prometheus 专用接口"""
    queryset = Message.objects.filter()
    serializer_class = PrometheusMessageSerializer
    authentication_classes = [PrometheusAuthentication]

    @staticmethod
    def get_loop_data(data):
        """根据 Meta loop 字段获取循环数据"""
        loop = 'alerts'  # 根据该字段循环
        data_list = list()

        if loop:
            jsonpath_expr = parse(loop)
            loop_data_list = [match.value for match in jsonpath_expr.find(data)]
            for loop_data in loop_data_list:
                if isinstance(loop_data, list):
                    data_list += loop_data
                elif isinstance(loop_data, dict):
                    data_list.append(loop_data)
                else:
                    pass
        else:
            data_list.append(data)

        return data_list

    def create(self, request, *args, **kwargs):
        response_data = list()
        for data in self.get_loop_data(request.data):
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_data.append(serializer.data)
        return Response({"data": response_data}, status=status.HTTP_201_CREATED)
