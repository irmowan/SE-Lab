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

		a1 = Assignments.objects.create(id="1", course=c1, name="离散作业1", description="群论", addTime=timezone.now(), deadlineTime=timezone.now()+timedelta(days=30))
		a2 = Assignments.objects.create(id="2", course=c1, name="离散作业2", description="命题逻辑", addTime=timezone.now(), deadlineTime=timezone.now()+timedelta(days=30))
		a3 = Assignments.objects.create(id="3", course=c2, name="进程死锁", description="进程死锁的四个必要条件", addTime=timezone.now(), deadlineTime=timezone.now()+timedelta(days=7))

		self.a1, self.a2, self.a3 = a1, a2, a3

		sub1 = Submissions.objects.create(assignment=a1, student=u3, content="群的定义是...", submissionTime=timezone.now())

	def test_index_case1(self):
		'''未登录'''
		client = Client()
		response = client.get('/user/1/homework/')
		self.assertEqual(type(response), django.http.response.HttpResponseRedirect)

	def test_index_case2(self):
		'''教师登录作业页面'''
		client = Client()
		client.post('/login/', data={'id': "12345678", 'password': "12345678"})
		response = client.get('/user/1/homework/')
		self.assertEqual(response.status_code, 200)
		response = client.get('/user/2/homework/')
		self.assertEqual(response.status_code, 404)

	def test_index_case3(self):
		'''学生登录作业页面'''
		client = Client()
		client.post('/login/', data={'id': "111111" , 'password': "111111"})
		response = client.get('/user/1/homework/')
		self.assertEqual(response.status_code, 200)
		response = client.get('/user/2/homework/')
		self.assertEqual(response.status_code, 404)

	def test_new_case1(self):
		'''未登录'''
		client = Client()
		response = client.get('/user/1/homework/new/')
		self.assertEqual(type(response), django.http.response.HttpResponseRedirect)

	def test_new_case2(self):
		'''学生不能创建作业'''
		client = Client()
		client.post('/login/', data={'id': "111111", 'password': "111111"})
		response = client.get('/user/1/homework/new/')
		self.assertEqual(response.status_code, 404)

	def test_new_case3(self):
		'''合法操作'''
		client = Client()
		client.post('/login/', data={'id': "123456", 'password': "123456"})
		response = client.get('/user/2/homework/new/')
		self.assertEqual(type(response), django.http.response.HttpResponse)

	def test_create_case1(self):
		'''未登录'''
		client = Client()
		response = client.post('/user/1/homework/new/create/', data={'assignmentName': '补充作业', 'description':'没有作业', 'createTime':timezone.now()});
		self.assertEqual(type(response), django.http.response.HttpResponseRedirect)

	def test_create_case2(self):
		'''学生尝试创建作业'''
		client = Client()
		client.post('/login/', data={'id': "111111", 'password': "111111"})
		response = client.post('/user/1/homework/new/create/', data={'assignmentName': '补充作业', 'description':'没有作业', 'createTime':timezone.now()});
		self.assertEqual(response.status_code, 404)

	def test_create_case3(self):
		'''尝试为非自己教授的课程创建作业'''
		client = Client()
		client.post('/login/', data={'id': "123456", 'password': '123456'})
		response = client.post('/user/1/homework/new/create/', data={'assignmentName': '补充作业', 'description':'没有作业', 'createTime':timezone.now()});
		self.assertEqual(response.status_code, 404)

	def test_create_case4(self):
		'''未填写作业详情'''
		client = Client()
		client.post('/login/', data={'id': "12345678", 'password': '12345678'})
		response = client.post('/user/1/homework/new/create/', data={});
		self.assertEqual(response.status_code, 404)

	def test_create_case5(self):
		'''合法操作：新建作业'''
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
		'''未登录'''
		client = Client()
		response = client.post('/user/1/homework/delete/', data={'id': 2})
		self.assertEqual(type(response), django.http.response.HttpResponseRedirect)

	def test_delete_case2(self):
		'''学生尝试删除作业'''
		client = Client()
		client.post('/login/', data={'id': '111111', 'password': '111111'})
		response = client.post('/user/1/homework/delete/', data={'id': 2})
		self.assertEqual(response.status_code, 404)

	def test_delete_case3(self):
		'''尝试删除非自己教授课程的作业'''
		client = Client()
		client.post('/login/', data={'id': '12345678', 'password': '12345678'})
		response = client.post('/user/2/homework/delete/', data={'id': 2})
		self.assertEqual(response.status_code, 404)
		response = client.post('/user/1/homework/delete/', data={'id': 2})
		self.assertEqual(response.status_code, 404)

	def test_delete_case4(self):
		'''尝试删除不存在的作业'''
		client = Client()
		client.post('/login/', data={'id': '12345678', 'password': '12345678'})
		response = client.post('/user/1/homework/delete/', data={'id': 8})
		self.assertEqual(response.status_code, 404)

	def test_delete_case5(self):
		'''合法操作：删除'''
		client = Client()
		client.post('/login/', data={'id': '12345678', 'password': '12345678'})
		response = client.post('user/1/homework/delete/', data={'id': 2})
		# TODO: fix
		self.assertQuerysetEqual(Assignments.objects.all(), [repr(a) for a in [self.a1, self.a3]])
		self.assertEqual(type(response), django.http.response.HttpResponseRedirect)

	def test_detail_case1(self):
		'''未登录'''
		client = Client()
		response = client.get('user/1/homework/1/')
		self.assertEqual(type(response), django.http.response.HttpResponseRedirect)

	def test_detail_case2(self):
		'''非本课程学生'''
		client = Client()
		client.post('/login/', data={'id': '111111', 'password': '111111'})
		response = client.get('user/1/homework/1/')
		self.assertEqual(response.status_code, 404)

	def test_detail_case3(self):
		'''课程号和作业号不对应'''
		client = Client()
		client.post('/login/', data={'id': '111111', 'password': '111111'})
		response = client.get('user/2/homework/1/')
		self.assertEqual(response.status_code, 404)

	def test_detail_case4(self):
		'''成功查看'''
		client = Client()
		client.post('/login/', data={'id': '111111', 'password': '111111'})
		response = client.get('user/1/homework/1/')
		data = response.json()
		self.assertEqual(data.get('assignmentName'), '离散作业1')

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
