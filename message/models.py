from django.db import models
from message.constants import LEVEL_CHOICES, STATUS_ALERT, STATUS_RECOVER
from model_utils.models import TimeStampedModel, StatusModel
from utils.common.models import UUIDModel
from utils.taggit.models import TaggedUUIDItem
from taggit.managers import TaggableManager
from model_utils.choices import Choices


# Create your models here.


class Message(UUIDModel, TimeStampedModel, StatusModel):
    """
    @data_source: 由 token 推断而来
    """
    STATUS = Choices(STATUS_ALERT, STATUS_RECOVER)
    project = models.CharField(verbose_name='项目标识', max_length=50)
    data_source = models.CharField(verbose_name='数据源', max_length=50, blank=True, null=True)
    type = models.CharField(verbose_name='消息标识', max_length=128)
    host = models.CharField(verbose_name='主机标识', max_length=128)
    title = models.CharField(verbose_name='消息标题', max_length=128)
    level = models.PositiveSmallIntegerField(verbose_name='消息等级', choices=LEVEL_CHOICES)
    raw = models.TextField(verbose_name='原始数据', blank=True, null=True)

    tags = TaggableManager(through=TaggedUUIDItem, blank=True)

    class Meta:
        verbose_name_plural = verbose_name = '- 消息管理'
        ordering = ['-created']

    def __str__(self):
        return self.title
