# -*- coding: utf-8 -*-

import django
from user.models import *
from course.models import *
from homework.models import *
from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client
from django.utils import timezone

# Create your tests here.

class HomeworkTest(TestCase):
	c1pk = ''
	c2pk = ''

	def setUp(self):
		setup_test_environment()

		u1 = Users.objects.create_user(id="12345678", password="12345678", name="赵一鸣", type="teacher")
		u2 = Users.objects.create_user(id="123456", password="123456", name="张亮", type="teacher")

		u3 = Users.objects.create_user(id="111111", password="111111", name="路人甲", type="student")
		u4 = Users.objects.create_user(id="111112", password="111111", name="路人乙", type="student")
		u5 = Users.objects.create_user(id="111113", password="111111", name="路人丙", type="student")
		u6 = Users.objects.create_user(id="111114", password="111111", name="路人丁", type="student")

		c1 = Courses.objects.create(name="离散数学", teacher=u1)
		c2 = Courses.objects.create(name="操作系统", teacher=u2)

		s1 = Selections.objects.create(course=c1, student=u3)
		s2 = Selections.objects.create(course=c1, student=u4)
		s3 = Selections.objects.create(course=c1, student=u5)

		a1 = Assignments.objects.create(course=c1, name="离散作业1", description="群论", addTime=timezone.now())
		a2 = Assignments.objects.create(course=c1, name="离散作业2", description="命题逻辑", addTime=timezone.now())

		sub1 = Submissions.objects.create(assignment=a1, student=u3, content="群的定义是...", submissionTime=timezone.now())

		self.c1pk = c1.pk
		self.c2pk = c2.pk

	def test_index(self):
		'''Test index page'''
		client = Client()
		response = client.get('/user/1/')

	def test_new(self):
		'''New a course'''
		client = Client()
		response = client.get('/user/1/homework/new/');
		self.assertEqual(type(response), django.http.response.HttpResponseRedirect)

		client = Client()
		client.post('/login/', data={'id': "111111", 'password': "111111"});
		response = client.get('/user/' + str(self.c1pk) + '/homework/new/')
		self.assertEqual(response.status_code, 404)

		client = Client()
		client.post('/login/', data={'id': "123456", 'password': "123456"});
		response = client.get('/user/' + str(self.c2pk) + '/homework/new/')
		self.assertEqual(type(response), django.http.response.HttpResponse)

	def test_create_case1(self):
		'''Create successfully'''
		client = Client()
		response = client.get('/user/1/homework/new/create/');
		self.assertEqual(type(response), django.http.response.HttpResponseRedirect)

	def test_create_case2(self):
		''''''
		pass

	def test_delete_case1(self):
		'''Delete succeed'''
		pass

	def test_delete_case2(self):
		'''Delete inexist course'''
		pass

	def test_delete_case3(self):
		'''Student try to delete course'''
		pass

	def test_detail_case1(self):
		''''''
		pass

	def test_detail_case2(self):
		''''''
		pass

	def test_update_case1(self):
		''''''
		pass

	def test_update_case2(self):
		''''''
		pass

	def test_submit_case1(self):
		''''''
		pass

	def test_submit_case2(self):
		''''''
		pass

	def test_submission_case1(self):
		''''''
		pass

	def test_submission_case2(self):
		''''''
		pass

	def test_score_case1(self):
		''''''
		pass

	def test_score_case2(self):
		''''''
		pass
