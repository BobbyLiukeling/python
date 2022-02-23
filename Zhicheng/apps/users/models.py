from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):#扩展用户信息数据库
    name = models.CharField(max_length=20,verbose_name='用户名',null=True, default=None)
    image = models.ImageField(upload_to='users/%Y/%m',verbose_name='用户头像',null=True, default=None)#这里给个破图
    profession = models.CharField(max_length=50,verbose_name='职业',null=True, default=None)
    city = models.CharField(max_length=50,verbose_name='城市')
    sign = models.CharField(max_length=50,verbose_name='个性签名',null=True, default=None)
    rand = models.CharField(choices=(('1','第一级'),('2','第二级'),('3','第三级')),default='1',verbose_name='用户等级',max_length=10)
    credit = models.IntegerField(verbose_name='积分',default=0)
    email = models.EmailField(max_length=30,verbose_name='邮箱',default='',null=True)
    mobile = models.CharField(max_length=11,verbose_name='手机号码')
    birthday = models.DateTimeField(verbose_name=u"生日", null=True, blank=True, default=None)
    gender = models.CharField(choices=(("male", u"男"), ("female", u"女")), default='male', max_length=6)
    add_time = models.DateTimeField(default=datetime.now,verbose_name='最近一次修改时间')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):#邮箱验证码
    identifying = models.CharField(max_length=20,verbose_name=u"验证码")
    email = models.EmailField(max_length=50,verbose_name=u"邮箱")
    send_type = models.CharField(max_length=10,choices=(("register",u"注册"),("forget",u"找回密码")))
    # default=datetime.now获取当时间（是程序运行时的时间），default=datetime.now（）将括号加上以后所获取的时间为程序编写的时间
    send_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}{1}{2}'.format(self.identifying," ",self.email)


class VerifyCodede(models.Model):
    identifying = models.CharField(max_length=6,verbose_name='验证码')
    mobile = models.CharField(max_length=11,verbose_name='电话号码')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"短信验证码"
        verbose_name_plural = verbose_name

    def __str__(self):#admin 管理时返回的题目标题
        return self.identifying

