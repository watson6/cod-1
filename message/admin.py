from django.contrib import admin
from message.models import Message


# Register your models here.

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['project', 'ds', 'host', 'type', 'title', 'level', 'status', 'time', 'created', 'modified']
    list_filter = ['status']
    search_fields = ['project', 'ds', 'host', 'type', 'title', 'raw']
    fieldsets = [
        ('基本信息', {'classes': ['grp-collapse grp-open'], 'fields': ['project', 'ds', 'host', 'type', 'title']}),
        ('状态管理', {'classes': ['grp-collapse grp-open'], 'fields': ['status', 'level']}),
        ('原始数据', {'classes': ['grp-collapse grp-open'], 'fields': ['raw']}),
    ]
