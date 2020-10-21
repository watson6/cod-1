import sys
import json
import logging
import requests
from abc import ABC, abstractmethod
from celery import shared_task
from datetime import timedelta
from message.models import Message
from message.constants import STATUS_ALERT, STATUS_RECOVER
from converge.models import BurrConverge
from event.models import Event
from event.constants import STATUS_NO_RESPONSE, STATUS_PROCESSING
from project.models import Project
from utils.common.constants import STATUS_PUBLISHED
from event.constants import STATUS_RESOLVED, STATUS_NOT_CLOSED, RES_TAG, DELAY_SEND_TAG, RESOURCE_TYPE
from actstream import action
from utils.env import Env
env = Env()

logger = logging.getLogger('root')
HOOK_COD = env.get('HOOK_COD')
HOOK_ON = env.get('HOOK_ON')


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


class MessageProcessor(ABC):
    """ 消息处理的基类"""

    def __init__(self, message: Message):
        self.message = message

    @abstractmethod
    def processor(self):
        pass

    @abstractmethod
    def results(self):
        pass


class MergeEventProcessor(MessageProcessor):
    """
    找到同类型的事件，自动合并到已存在的事件里面。找不到的话，则会返回空不处理。
    """

    def processor(self):
        # last_event = self.message.last_event()
        last_event = Event.objects.filter(host=self.message.host, is_enabled=True,
                                          tags__name='type:%s' % self.message.type,
                                          project__project=self.message.project,
                                          status__in=STATUS_NOT_CLOSED).order_by('create').last()
        if last_event:
            # 合并已知事件
            last_event.messages.add(self.message)
            if self.message.type in RESOURCE_TYPE:
                last_event.tags.add(RES_TAG)
            self.message.converged = True
            self.message.save()
            logger.info('merge to event. {}'.format(last_event.name))
            return last_event
        else:
            return None

    def results(self):
        if self.processor():
            return True, None
        else:
            return False, None


class CreateEventProcessor(MessageProcessor):
    """
    基于当前的消息进行创建关联事件，事件包括如下元素：项目、主机、标题、告警等级
    """

    def processor(self):
        project = Project.objects.get(project=self.message.project)
        # 创建事件。事件关联的信息，以消息关联的字段来组装信息。项目和主机host是最小的事件维度。
        event = Event.objects.create(project=project,
                                     host=self.message.host,
                                     name=self.message.title,
                                     level=self.message.level)
        # 添加事件流
        action.send(sender=project,
                    verb='项目, 创建告警事件', action_object=event, target=event, status='create event success')
        # 添加事件关联的收敛规则
        event.messages.add(self.message)
        # 关联tags标签字段
        event.tags.add('type:%s' % self.message.type)
        self.message.converged = True  # 关闭消息收敛
        self.message.save()
        event.get_upgrade()
        return event

    def results(self):
        event = self.processor()
        if event:
            return False, event
        else:
            return True, None


def handle_message_recover(message: Message) -> None:
    """
    处理异常告警恢复
    :param message: 当前事件消息
    """
    events = Event.objects.filter(project__name=message.project, host=message.host, status__in=STATUS_NOT_CLOSED,
                                  tags__name='type:%s' % message.type)
    if events:
        # 对告警类型为恢复状态的单条消息，修改收敛状态。
        message.converged = True
        message.save()
        # 判断事件如果有关联资源标签，则不发送告警
        if not events.last().check_similar_event(similar=1):
            # 发送告警通知
            # recovery_notifications(events)
            pass
        else:
            for event in events:
                event.tags.add(DELAY_SEND_TAG)
        # 事件状态更新为:告警恢复，关闭事件
        events.update(status=STATUS_RESOLVED)
        logger.info('recovery event success,IP: ' + message.host)
        # 告警恢复事件流
        for event in events:
            action.send(sender=event, verb='事件, 告警恢复', action_object=event, target=event,
                        status='recovery event success')


# 推送消息到COD调试环境
def post_message(message):
    play_data = {
        "project": message.project,
        "type": message.type,
        "host": message.host,
        "title": message.title,
        "level": str(message.level),
        "status": str(message.status),
        "time": message.time.strftime('%Y-%m-%d %H:%M:%S'),
    }
    headers = {"Authorization": "token 92369754-44a1-476e-a16a-767aa4045c74"}
    try:
        response = requests.post(url=HOOK_COD, headers=headers, data=play_data)
        logging.info('Post Hook COD, status %s, Hook cod %s, Hook on %s' % (response.status_code, HOOK_COD, HOOK_ON))
    except requests.exceptions.ConnectionError:
        logging.error('push message hook server connection error')

# @shared_task(ignore_result=True)
# def message_handler(message_id) -> None:
#     """
#     告警消息异步处理：告警收敛
#     @param message_id: Message Object Id
#     @return: None
#     """
#     # 配置告警消息收敛策略
#     # 这个配置暂时放在此处，未来有多种策略时移到 django.conf.settings 中
#     # 配置使用字符串形式避免后期迁移配置时类型导入
#     strategies = ['MessageBurrConvergeStrategy']
#
#     # 获取上报告警消息对象
#     message = Message.objects.get(id=message_id)
#
#     # 循环消息收敛策略
#     for strategy_str in strategies:
#         strategy_class = getattr(sys.modules[__name__], strategy_str)
#         strategy_instance = strategy_class(message=message)
#         strategy_instance.do_converge()


@shared_task(ignore_result=True)
def message_handler(message_id) -> None:
    """
    告警消息异步处理：告警收敛
    @param message_id: Message Object Id
    @return: None
    """

    # 这个配置暂时放在此处，未来有多种策略时移到 django.conf.settings 中
    # 配置使用字符串形式避免后期迁移配置时类型导入
    processors = ['MergeEventProcessor',  # 合并已知事件
                  'CreateEventProcessor',  # 创建事件
                  ]

    # 获取上报告警消息对象
    message = Message.objects.get(id=message_id)
    logger.info('message come on ... ')

    if message.status == STATUS_ALERT:
        event = None
        # 循环消息收敛策略
        for processor in processors:
            processor_class = getattr(sys.modules[__name__], processor)
            processor_instance = processor_class(message=message)
            # 判断有状态则直接break 列表循环，无状态时，则是进入创建事件操作
            result_status, event = processor_instance.results()
            if result_status:
                break
        # 生成新的事件之后，进行判断告警
        if event:
            if not event.check_similar_event(similar=2):
                # 告警发送及升级
                # upgrading(event.id)
                pass
            else:
                # 同类事件取消告警之后增加延迟发送标签
                event.tags.add(DELAY_SEND_TAG)
                # 取消同类事件发送
                action.send(sender=event,
                            verb='事件, 同类高发事件', action_object=event, target=event, status='同类高发事件取消发送消息')

    elif message.status == STATUS_RECOVER:
        handle_message_recover(message)
    else:
        return None

    # 消息钩子，推送到开发环境调试
    # if HOOK_ON == 'true':
    #     post_message(message)
