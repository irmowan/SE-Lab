# -*- coding: utf-8 -*-

import django
from user.models import *
from course.models import *
from django.db import models
from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client
import json

# Create your tests here.

class CourseTests(TestCase):
	c1pk = ''
	c2pk = ''

	def setUp(self):
		setup_test_environment()
		u1 = Users.objects.create_user(id="12345678", password="12345678", name="赵一鸣", type="teacher")
		u2 = Users.objects.create_user(id="123456", password="123456", name="张亮", type="teacher")

		u3 = Users.objects.create_user(id="111111", password="111111", name="路人甲", type="student")
		u4 = Users.objects.create_user(id="111112", password="111111", name="路人乙", type="student")
		u5 = Users.objects.create_user(id="111113", password="111111", name="路人丙", type="student")

		c1 = Courses.objects.create(name="离散数学", teacher=u1)
		c2 = Courses.objects.create(name="操作系统", teacher=u2)

		s1 = Selections.objects.create(course=c1, student=u3)
		s2 = Selections.objects.create(course=c2, student=u4)
		s3 = Selections.objects.create(course=c2, student=u5)

		self.c1pk = c1.pk
		self.c2pk = c2.pk

	def test_index_case1(self):
		"""用户未登录"""
		client = Client()
		response = client.get('/user/1/');
		self.assertEqual(response.status_code, 302)
		self.assertEqual(type(response), django.http.response.HttpResponseRedirect)

	def test_index_case2(self):
		"""测试教师"""
		client = Client()
		client.post('/login/', data={'id': "123456", 'password': "123456"})
		response = client.get('/user/' + str(self.c1pk) + '/')
		self.assertEqual(response.status_code, 404)

		response = client.get('/user/' + str(self.c2pk) + '/')
		self.assertEqual(type(response), django.http.response.HttpResponse)
		data = json.loads(response.content.decode('utf-8'))
		self.assertEqual(data['name'], u'操作系统')
		self.assertEqual(data['count'], 2)

	def test_index_case3(self):
		"""测试学生"""
		client = Client()
		client.post('/login/', data={'id': "111111", 'password': "111111"})
		response = client.get('/user/' + str(self.c2pk) + '/')
		self.assertEqual(response.status_code, 404)

		response = client.get('/user/' + str(self.c1pk) + '/')
		self.assertEqual(type(response), django.http.response.HttpResponse)
		data = json.loads(response.content.decode('utf-8'))
		self.assertEqual(data['name'], u'离散数学')
		self.assertEqual(data['teacherName'], u'赵一鸣')
