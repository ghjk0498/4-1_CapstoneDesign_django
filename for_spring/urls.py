# -*- coding: utf-8 -*-

from django.urls import include, re_path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'test', views.TestViewSet)

urlpatterns = [
    re_path(r'^', include(router.urls)),
    re_path('api-auth/', include('rest_framework.urls'))
]