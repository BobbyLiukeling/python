from django.db import models
from datetime import datetime
from DjangoUeditor.models import UEditorField

from users.models import UserProfile
# from Zhicheng.sittings import LOCATION

# Create your models here.

class Label(models.Model):
    label = models.CharField(max_length=50,verbose_name='标签')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.label


class Article(models.Model):
    user = models.ForeignKey(UserProfile,verbose_name='用户',on_delete=models.CASCADE)
    city = models.CharField(max_length=50,verbose_name='城市')#必填字段
    label = models.ForeignKey(Label,verbose_name='标签',on_delete=models.CASCADE)#必填字段
    title = models.CharField(max_length=20,verbose_name='文章标题')#必填字段
    content = UEditorField(verbose_name=u'课程详情',imagePath="article/ueditor/",default='')
    file = models.FileField(verbose_name='文章附件',upload_to='article/ueditor/',blank=True,null=True)
    click_nums = models.IntegerField(default=0,verbose_name='文章点击数')
    fav_nums = models.IntegerField(default=0,verbose_name='文章收藏数')
    add_time = models.DateTimeField(default=datetime.now)
    update_time = models.DateTimeField(default=datetime.now,verbose_name='最近一次修改时间')

    class Meta:
        verbose_name = u"文章"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


# class Position(models.Model):
#     COUNTRY = [(key, key) for key in LOCATION.items()]
#     country = models.CharField(max_length=50, null=True, blank=True, verbose_name='城市', choices=COUNTRY)

class Comment(models.Model):
    commenter = models.ForeignKey(UserProfile,verbose_name='评论者',on_delete=models.CASCADE,related_name='commenter')
    article = models.ForeignKey(Article,verbose_name='文章',on_delete=models.CASCADE)
    comment_content = models.TextField(verbose_name='评论内容')
    fav_nums = models.IntegerField(default=0,verbose_name='点赞数')
    accept_nums = models.IntegerField(default=0,verbose_name='采纳数')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='评论时间')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}{1}{2}'.format(self.commenter.username,'  ',self.article.title)


class Replay(models.Model):#回复讨论
    comment = models.ForeignKey(Comment,verbose_name='文章回复',on_delete=models.CASCADE)
    replay_contenter = models.ForeignKey(UserProfile,verbose_name='讨论人',on_delete=models.CASCADE)
    replay_content = models.TextField(verbose_name='回复讨论内容')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='讨论时间')

    class Meta:
        verbose_name = '回复讨论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.replay_contenter.username


