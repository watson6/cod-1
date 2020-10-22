from django.db import models
from utils.common.models import OwnerModel
from model_utils.models import TimeStampedModel, SoftDeletableModel, UUIDModel
from project.models import Project


# Create your models here.


class Silence(UUIDModel, OwnerModel, TimeStampedModel, SoftDeletableModel):
    """短期沉默规则"""
    project = models.ForeignKey(Project, verbose_name='项目名称', on_delete=models.CASCADE)
    filter_kwargs = models.TextField(verbose_name='沉默规则', blank=True, null=True)
    ignore_type = models.BooleanField(verbose_name='忽略类型', default=False)
    duration = models.PositiveSmallIntegerField(verbose_name='沉默时间', default=60)

    class Meta:
        verbose_name_plural = verbose_name = '- 沉默规则'

    def __str__(self):
        return "%s_%d 分钟" % (self.project.name, self.duration)
