# -*- coding: utf-8 -*-

import django
from user.models import *
from django.db import models
from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client

# Create your tests here.

class UserViewTests(TestCase):
	def setUp(self):
		setup_test_environment()
		u1 = Users.objects.create_user(id="123456", password="123456", name="张亮", type="teacher")
		u2 = Users.objects.create_user(id="123457", password="123457", name="毕业狗", type="student")
		u2.is_active = False
		u2.save()

	def test_login_case1(self):
		client = Client()
		response = client.post('/login/', data={'id': "123456", 'password': "123456"})
		self.assertEqual(response.status_code, 302)
		self.assertEqual(type(response), django.http.response.HttpResponseRedirect)
		self.assertEqual(response.url, '/user/')

	def test_login_case2(self):
		client = Client()
		response = client.post('/login/', data={'id': "123456", 'password': "1234567"})
		self.assertEqual(response.status_code, 200)
		self.assertEqual(type(response), django.http.response.HttpResponse)
		self.assertEqual(response.content, b"Login fail!")

	def test_login_case3(self):
		client = Client()
		response = client.post('/login/', data={'id': "123457", 'password': "123457"})
		self.assertEqual(response.status_code, 200)
		self.assertEqual(type(response), django.http.response.HttpResponse)
		self.assertEqual(response.content, b"Fail: a disabled account")
