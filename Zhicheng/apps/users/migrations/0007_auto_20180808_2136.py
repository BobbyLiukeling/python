# Generated by Django 2.0.4 on 2018-08-08 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20180807_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(default='', max_length=30, null=True, verbose_name='邮箱'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default=None, null=True, upload_to='users/%Y/%m', verbose_name='用户头像'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(default=None, max_length=20, null=True, verbose_name='用户名'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profession',
            field=models.CharField(default=None, max_length=50, null=True, verbose_name='职业'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='sign',
            field=models.CharField(default=None, max_length=50, null=True, verbose_name='个性签名'),
        ),
    ]