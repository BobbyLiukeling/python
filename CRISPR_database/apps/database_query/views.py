from django.shortcuts import render

# Create your views here.


from django.views.generic.base import View
from django.http import HttpResponse
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins,generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter


from .models import CRISPR
from .serializers import CRISPRSerializer
from .filter import CRISPRFilter

import pdb


#以下是三种view的写法

# class CRISPRView(APIView):
#
#     def get(self,request):
#         CRISPRs = CRISPR.objects.all()
#         CRISPR_serializer = CRISPRSerializer(CRISPRs,many=True)
#         return Response(CRISPR_serializer.data)


# class CRISPRView(mixins.ListModelMixin,generics.GenericAPIView):
#     queryset = CRISPR.objects.all()
#     serializer_class = CRISPRSerializer
#
#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)


class CRISPRView(generics.ListAPIView):
    queryset = CRISPR.objects.all()
    serializer_class = CRISPRSerializer

    #过滤器
    filter_backends = (DjangoFilterBackend,SearchFilter,OrderingFilter)
    filter_class = CRISPRFilter
    #搜索，模糊查询
    search_fields = ('CRISPR_name','Organism','CRISPR_type','PAM_Consensus','PAM_Length')
    #排序
    ordering_fields = ('CRISPR_type','PAM_Length','PAM_Consensus')



