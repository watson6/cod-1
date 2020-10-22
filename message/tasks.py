import sys
import json
import logging
from abc import ABC, abstractmethod
from celery import shared_task
from datetime import timedelta
from message.models import Message
from message.constants import STATUS_ALERT, STATUS_RECOVER
from converge.models import BurrConverge
from event.models import Event
from event.constants import STATUS_NO_RESPONSE, STATUS_PROCESSING
from utils.common.constants import STATUS_PUBLISHED

logger = logging.getLogger('root')


class MessageConvergeStrategy(ABC):
    """消息收敛策略纯虚接口类"""

    def __init__(self, message: Message, *args, **kwargs) -> None:
        """
        @param message: 待处理消息实例
        @return: None
        """
        self.message = message
        self.MAPPING = {
            STATUS_ALERT: self.status_alert_handler,
            STATUS_RECOVER: self.status_recover_handler
        }

    def do_converge(self):
        handler = self.MAPPING[self.message.status]
        handler()

    @abstractmethod
    def status_alert_handler(self) -> None:
        pass

    @abstractmethod
    def status_recover_handler(self) -> None:
        pass


class MessageBurrConvergeStrategy(MessageConvergeStrategy):
    """消息毛刺收敛策略"""

    def __init__(self, message: Message, *args, **kwargs) -> None:
        """
        @param message: 待处理消息实例
        @return: None
        """
        self.converges = BurrConverge.objects.filter(status=STATUS_PUBLISHED,
                                                     is_removed=False,
                                                     project__name=self.message.project)
        super(MessageBurrConvergeStrategy, self).__init__(message)

    def status_alert_handler(self) -> None:
        """
        告警消息收敛处理步骤
        1. 获取最近的未关闭同类型事件
        2. 如果存在未关闭同类事件，则直接添加当前消息到该事件
        3. 如果不存在未关闭同类事件，则根据收敛条件判断是否创建新事件
        """
        # 1. 检查是否存在未关闭的相关事件
        last_event = Event.objects.filter(ds=self.message.ds,
                                          host=self.message.host,
                                          project__name=self.message.project,
                                          status__in=[STATUS_NO_RESPONSE, STATUS_PROCESSING]
                                          ).order_by('created').last()
        # 判断是否存在未关闭的收敛事件
        if last_event:
            # 2. 如果存在未关闭同类事件，则直接添加当前消息到该事件
            last_event.messages.add(self.message)
        else:
            # 3. 如果不存在未关闭同类事件，则根据收敛条件判断是否创建新事件
            for converge in self.converges:
                self.message_do_converge(converge)

    def message_do_converge(self, converge: BurrConverge) -> None:
        """
        告警消息执行收敛规则
        @param converge: 具体要执行的收敛规则
        @return: None
        """
        kwargs = json.loads(converge.filter_kwargs)
        converge_time = self.message.created - timedelta(minutes=converge.section)
        messages = Message.objects.filter(project=converge.project.name,
                                          host=self.message.host,
                                          ds=self.message.ds,
                                          created__lte=self.message.created,
                                          created__gte=converge_time,
                                          ).filter(**kwargs).all()
        # 如果查询到的消息数量大于阈值，则创建新事件
        if messages.count() > converge.count:
            pass

    def status_recover_handler(self):
        """告警恢复消息处理"""
        pass


@shared_task(ignore_result=True)
def message_handler(message_id) -> None:
    """
    告警消息异步处理：告警收敛
    @param message_id: Message Object Id
    @return: None
    """
    # 配置告警消息收敛策略
    # 这个配置暂时放在此处，未来有多种策略时移到 django.conf.settings 中
    # 配置使用字符串形式避免后期迁移配置时类型导入

    print(message_id)
    # strategies = ['MessageBurrConvergeStrategy']
    #
    # # 获取上报告警消息对象
    # message = Message.objects.get(id=message_id)
    #
    # # 循环消息收敛策略
    # for strategy_str in strategies:
    #     strategy_class = getattr(sys.modules[__name__], strategy_str)
    #     strategy_instance = strategy_class(message=message)
    #     strategy_instance.do_converge()
