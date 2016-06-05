# -*- coding: utf-8 -*-

import django
from user.models import *
from course.models import *
from homework.models import *
from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client
from django.utils import timezone
from datetime import timedelta

# Create your tests here.

class HomeworkTest(TestCase):
	def setUp(self):
		setup_test_environment()

		u1 = Users.objects.create_user(id="12345678", password="12345678", name="赵一鸣", type="teacher")
		u2 = Users.objects.create_user(id="123456", password="123456", name="张亮", type="teacher")

		u3 = Users.objects.create_user(id="111111", password="111111", name="路人甲", type="student")
		u4 = Users.objects.create_user(id="111112", password="111111", name="路人乙", type="student")
		u5 = Users.objects.create_user(id="111113", password="111111", name="路人丙", type="student")
		u6 = Users.objects.create_user(id="111114", password="111111", name="路人丁", type="student")

		c1 = Courses.objects.create(id="1", name="离散数学", teacher=u1)
		c2 = Courses.objects.create(id="2", name="操作系统", teacher=u2)

		s1 = Selections.objects.create(course=c1, student=u3)
		s2 = Selections.objects.create(course=c1, student=u4)
		s3 = Selections.objects.create(course=c1, student=u5)

		a1 = Assignments.objects.create(course=c1, name="离散作业1", description="群论", addTime=timezone.now(), deadlineTime=timezone.now()+timedelta(days=30))
		a2 = Assignments.objects.create(course=c1, name="离散作业2", description="命题逻辑", addTime=timezone.now(), deadlineTime=timezone.now()+timedelta(days=30))

		sub1 = Submissions.objects.create(assignment=a1, student=u3, content="群的定义是...", submissionTime=timezone.now())

	def test_index_case1(self):
		'''Not login in'''
		client = Client()
		response = client.get('/user/1/homework/')
		self.assertEqual(type(response), django.http.response.HttpResponseRedirect)

	def test_index_case2(self):
		'''Test index page of teacher'''
		client = Client()
		client.post('/login/', data={'id': "12345678", 'password': "12345678"})
		response = client.get('/user/1/homework/')
		self.assertEqual(response.status_code, 200)
		response = client.get('/user/2/homework/')
		self.assertEqual(response.status_code, 404)

	def test_index_case3(self):
		'''Test index page of student'''
		client = Client()
		client.post('/login/', data={'id': "111111" , 'password': "111111"})
		response = client.get('/user/1/homework/')
		self.assertEqual(response.status_code, 200)
		response = client.get('/user/2/homework/')
		self.assertEqual(response.status_code, 404)

	def test_new_case1(self):
		'''Not login in'''
		client = Client()
		response = client.get('/user/1/homework/new/')
		self.assertEqual(type(response), django.http.response.HttpResponseRedirect)

	def test_new_case2(self):
		'''Operation fail'''
		client = Client()
		client.post('/login/', data={'id': "111111", 'password': "111111"})
		response = client.get('/user/1/homework/new/')
		self.assertEqual(response.status_code, 404)

	def test_new_case3(self):
		'''Operation succeed'''
		client = Client()
		client.post('/login/', data={'id': "123456", 'password': "123456"})
		response = client.get('/user/2/homework/new/')
		self.assertEqual(type(response), django.http.response.HttpResponse)

	def test_create_case1(self):
		'''Not login in'''
		client = Client()
		response = client.post('/user/1/homework/new/create/', data={'assignmentName': '补充作业', 'description':'没有作业', 'createTime':timezone.now()});
		self.assertEqual(type(response), django.http.response.HttpResponseRedirect)

	def test_create_case2(self):
		'''Student try to create'''
		client = Client()
		client.post('/login/', data={'id': "111111", 'password': "111111"})
		response = client.post('/user/1/homework/new/create/', data={'assignmentName': '补充作业', 'description':'没有作业', 'createTime':timezone.now()});
		self.assertEqual(response.status_code, 404)

	def test_create_case3(self):
		'''Other teacher try to create'''
		client = Client()
		client.post('/login/', data={'id': "123456", 'password': '123456'})
		response = client.post('/user/1/homework/new/create/', data={'assignmentName': '补充作业', 'description':'没有作业', 'createTime':timezone.now()});
		self.assertEqual(response.status_code, 404)

	def test_create_case4(self):
		'''Create fail'''
		client = Client()
		client.post('/login/', data={'id': "12345678", 'password': '12345678'})
		response = client.post('/user/1/homework/new/create/', data={});
		self.assertEqual(response.status_code, 404)

	def test_create_case5(self):
		'''Create succeed'''
		client = Client()
		client.post('/login/', data={'id': "12345678", 'password': '12345678'})
		response = client.post('/user/1/homework/new/create/', data={'assignmentName': '补充作业', 'description':'没有作业', 'createTime':timezone.now()});
		self.assertEqual(type(response), django.http.response.HttpResponseRedirect)
		try:
			new_assignment = Assignments.objects.get(name='补充作业')
		except Assignments.DoesNotExist:
			new_assignment = None
		self.assertEqual(new_assignment.name, '补充作业')

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
