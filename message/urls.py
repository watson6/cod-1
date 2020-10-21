from rest_framework.routers import DefaultRouter
from django.urls import path, include
from message.views import RestAPIMessageViewSets

router = DefaultRouter()
router.register(r'restapi', RestAPIMessageViewSets)

urlpatterns = [
    path('', include(router.urls)),
]
