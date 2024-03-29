﻿#! /usr/bin/env python

import django
django.setup()

from user.models import *
from course.models import *
from homework.models import *
from django.contrib import auth
from datetime import datetime

if __name__ == "__main__":
    u1 = Users.objects.create_user(id="13307130319", password="qwerty", name="Xiaotao Liang", type="student")
    u2 = Users.objects.create_user(id="12345678", password="12345678", name="赵一鸣", type="teacher")
    u3 = Users.objects.create_user(id="123456", password="123456", name="张亮", type="teacher")
    u4 = Users.objects.create_user(id="111111", password="111111", name="路人甲", type="student")
    u5 = Users.objects.create_user(id="222222", password="222222", name="陈利锋", type="teacher")
    u6 = Users.objects.create_user(id="333333", password="333333", name="StudentA", type="student")
    u7 = Users.objects.create_user(id="444444", password="444444", name="StudentB", type="student")
    u8 = Users.objects.create_user(id="555555", password="555555", name="StudentC", type="student")

    c1 = Courses.objects.create(name="离散数学", teacher=u2)
    c2 = Courses.objects.create(name="操作系统", teacher=u3)
    c3 = Courses.objects.create(name="计算机体系结构", teacher=u5)

    s1 = Selections.objects.create(course=c1, student=u1)
    s2 = Selections.objects.create(course=c1, student=u4)
    s3 = Selections.objects.create(course=c3, student=u1)
    s3 = Selections.objects.create(course=c3, student=u4)
    s4 = Selections.objects.create(course=c1, student=u6)
    s5 = Selections.objects.create(course=c1, student=u7)
    s6 = Selections.objects.create(course=c1, student=u8)

    ass1 = Assignments.objects.create(course=c1, name="群", description="证明阿贝尔群...", addTime=datetime.now(), deadlineTime=datetime(2016, 12, 1, 23, 59))
    ass2 = Assignments.objects.create(course=c1, name="环", description="证明环的理想...", addTime=datetime.now(), deadlineTime=datetime(2016, 12, 1, 23, 59))
    ass3 = Assignments.objects.create(course=c3, name="DLX16设计报告", description="WTF", addTime=datetime.now(), deadlineTime=datetime(2016, 12, 1, 23, 59))
    ass4 = Assignments.objects.create(course=c3, name="DLX16设计报告", description="WTF", addTime=datetime.now(), deadlineTime=datetime(2016, 12, 1, 23, 59))

    sub1 = Submissions.objects.create(assignment=ass1, student=u1, content="设群A...", submissionTime=datetime.now(), score=1, comments="")
    sub2 = Submissions.objects.create(assignment=ass1, student=u4, content="设群A...", submissionTime=datetime.now(), score=12, comments="")
    sub3 = Submissions.objects.create(assignment=ass3, student=u1, content="cpu16.vhd", submissionTime=datetime.now(), score=100, comments="")
