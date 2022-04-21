# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'test', views.TestViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url('api-auth/', include('rest_framework.urls'))
]