#!/usr/bin/env python
# encoding: utf-8
'''
@author: bobby
@file: filter.py
@time: 7/23/20 7:33 PM
'''

#过滤器

import django_filters

from .models import CRISPR

class CRISPRFilter(django_filters.rest_framework.FilterSet):
    '''
    数据过滤
    通过过滤ＰＡＭ长度过滤
    '''

    PAM_Length_min = django_filters.NumberFilter(field_name='PAM_Length',lookup_expr='gte')
    PAM_Length_max = django_filters.NumberFilter(field_name='PAM_Length',lookup_expr='lte')

    class Meta:
        model = CRISPR
        fields = ['PAM_Length_min','PAM_Length_max']
