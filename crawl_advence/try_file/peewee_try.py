# -*- encoding: utf-8 -*-
# @author : bobby
# @time : 2020/5/17 23:47

from peewee import *

db = SqliteDatabase('people.db')

class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db # This model uses the "people.db" database.