# Generated by Django 2.0.4 on 2018-08-07 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_userprofile_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emailverifyrecord',
            old_name='code',
            new_name='identifying',
        ),
        migrations.RenameField(
            model_name='verifycodede',
            old_name='code',
            new_name='identifying',
        ),
    ]
