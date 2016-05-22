﻿#!/usr/bin/env python

from user.models import *
from course.models import *
from homework.models import *
from django.contrib import auth

u1 = Users.objects.create_user(id="13307130319", password="qwerty", name="Xiaotao Liang", type="student")
u2 = Users.objects.create_user(id="12345678", password="12345678", name="赵一鸣", type="teacher")
u3 = Users.objects.create_user(id="123456", name="张亮", type="teacher")
u4 = Users.objects.create_user(id="111111", name="路人甲", type="student")
u5 = Users.objects.create_user(id="222222", name="陈立峰", type="teacher")

c1 = Courses.objects.create(name="离散数学", teacher=u2)
c2 = Courses.objects.create(name="操作系统", teacher=u3)
c3 = Courses.objects.create(name="计算机体系结构", teacher=u5)

s1 = Selections.objects.create(course=c1, student=u1)
s2 = Selections.objects.create(course=c1, student=u4)
s3 = Selections.objects.create(course=c3, student=u1)