"""Zhicheng URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.static import serve
import xadmin
from django.urls import path,include,re_path
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token
from .settings import MEDIA_ROOT
from users.views import SmsCodeView,RegisterViewSet,LoginViewset
from rest_framework.authtoken import views

router = DefaultRouter()

#发送手机验证码
router.register('identify',SmsCodeView,base_name='identify')

#注册
router.register('register',RegisterViewSet,base_name='register')

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('ueditor/',include('DjangoUeditor.urls' )),
    path('captcha/',include('captcha.urls')),#验证码，未用

    path('api_auth',include('rest_framework.urls')),#无用
    path('',include(router.urls)),

    re_path(r'^media/(?P<path>.*)$', serve, { 'document_root': MEDIA_ROOT,}),#图片上传路径
    # path('login',obtain_jwt_token,name = 'login'),
    path('login/',LoginViewset.as_view(),name = 'login'),#重写了JWT方法

    #文档
    path('docs/',include_docs_urls('Zhicheng')),
    path('api-token-auth/', views.obtain_auth_token)
]
