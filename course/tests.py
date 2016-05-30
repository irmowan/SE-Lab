# -*- coding: utf-8 -*-

import django
import views
from user.models import *
from course.models import *
from django.db import models
from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client


# Create your tests here.

class CourseIndexTests(TestCase):
	c1pk = ''
	c2pk = ''

	def setUp(self):
		setup_test_environment()
		u2 = Users.objects.create_user(id="12345678", password="12345678", name="赵一鸣", type="teacher")
		u3 = Users.objects.create_user(id="123456", password="123456", name="张亮", type="teacher")
		u4 = Users.objects.create_user(id="111111", password="111111", name="路人甲", type="student")
		c1 = Courses.objects.create(name="离散数学", teacher=u2)
		c2 = Courses.objects.create(name="操作系统", teacher=u3)
		s2 = Selections.objects.create(course=c1, student=u4)
		self.c1pk = c1.pk
		self.c2pk = c2.pk

	def test_index(self):
		client = Client()
		response = client.get('/user/1/');
		self.assertEqual(type(response), django.http.response.HttpResponseRedirect)
		self.assertEqual(response.url, '/?next=/user/1/')
		
		client = Client()
		client.post('/login/', data={'id': "123456", 'password': "123456"});
		response = client.get('/user/' + str(self.c1pk) + '/')
		self.assertEqual(type(response), django.http.response.HttpResponseNotFound)
		self.assertEqual(response.status_code, 404)

		response = client.get('/user/' + str(self.c2pk) + '/')
		self.assertEqual(type(response), django.http.response.HttpResponse)

		client = Client()
		client.post('/login/', data={'id': "111111", 'password': "111111"});
		response = client.get('/user/' + str(self.c2pk) + '/')
		self.assertEqual(type(response), django.http.response.HttpResponseNotFound)
		self.assertEqual(response.status_code, 404)

		response = client.get('/user/' + str(self.c1pk) + '/')
		self.assertEqual(type(response), django.http.response.HttpResponse)


		
		