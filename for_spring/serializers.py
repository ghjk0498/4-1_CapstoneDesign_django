# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 19:17:14 2022

@author: User
"""

from rest_framework import serializers
from .models import Test


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ('id', 'title', 'text', 'image', 'csv')
