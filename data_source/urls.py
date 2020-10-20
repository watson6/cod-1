from django.urls import path, include
from rest_framework.routers import DefaultRouter

from data_source.views import WebHookMessageViewSets, PrometheusMessageViewSets

router = DefaultRouter()
router.register(r'prometheus', PrometheusMessageViewSets)
router.register(r'webhook', WebHookMessageViewSets)

urlpatterns = [
    path('', include(router.urls)),
]
