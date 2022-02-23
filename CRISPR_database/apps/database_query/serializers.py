#!/usr/bin/env python
# encoding: utf-8
'''
@author: bobby
@file: serializers.py
@time: 7/20/20 3:16 AM
'''

#APIview　方法实现后台ｐｏｓｔ到前端页面
from rest_framework import serializers

from .models import CRISPR


class CRISPRSerializer(serializers.ModelSerializer):
    class Meta:
        model = CRISPR
        fields = '__all__'


