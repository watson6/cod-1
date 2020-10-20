from django.urls import path, include
from rest_framework.routers import DefaultRouter

from data_source.views import RestAPIMessageViewSets, PrometheusMessageViewSets

router = DefaultRouter()
router.register(r'prometheus', PrometheusMessageViewSets)
router.register(r'restapi', RestAPIMessageViewSets)

urlpatterns = [
    path('', include(router.urls)),
]
