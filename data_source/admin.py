from django.contrib import admin
from data_source.models import DataSource


# Register your models here.


class DataSourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'label', 'auto_close', 'close_after', 'status', 'is_removed', 'created', 'modified']
    list_filter = ['is_removed', 'status']
    search_fields = ['name', 'label']
    fieldsets = [
        ('基本信息', {'classes': ['grp-collapse grp-open'], 'fields': ['name', 'label', 'close_after']}),
        ('时间管理', {'classes': ['grp-collapse grp-open'], 'fields': ['created', 'modified']}),
        ('状态管理', {'classes': ['grp-collapse grp-open'], 'fields': ['status', 'is_removed', 'auto_close']}),
    ]
