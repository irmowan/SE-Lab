# -*- coding: utf-8 -*-

import django
from user.models import *
from course.models import *
from homework.models import *
from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client
from django.utils import timezone
import json

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

		self.s3pk = u3.pk

		c1 = Courses.objects.create(name="离散数学", teacher=u1)
		c2 = Courses.objects.create(name="操作系统", teacher=u2)

		s1 = Selections.objects.create(course=c1, student=u3)
		s2 = Selections.objects.create(course=c1, student=u4)
		s3 = Selections.objects.create(course=c1, student=u5)

		self.subtime = timezone.now();
		a1 = Assignments.objects.create(course=c1, name="离散作业1", description="群论", addTime=self.subtime)
		a2 = Assignments.objects.create(course=c1, name="离散作业2", description="命题逻辑", addTime=self.subtime)

		sub1 = Submissions.objects.create(assignment=a1, student=u3, content="群的定义是...", submissionTime=self.subtime)

		self.c1pk = c1.pk
		self.c2pk = c2.pk
		self.a1pk = a1.pk
		self.sub1pk = sub1.pk

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
		'''没登录'''
		client = Client()
		response = client.post('/user/' + str(self.c1pk) + '/homework/' + str(self.a1pk) + '/update/'
								, data = {});
		self.assertEqual(type(response), django.http.response.HttpResponseRedirect)
		pass

	def test_update_case2(self):
		'''学生身份登陆'''
		client = Client()
		client.post('/login/', data={'id': "111111", 'password': "111111"});
		response = client.post('/user/' + str(self.c1pk) + '/homework/' + str(self.a1pk) + '/update/'
								, data = {});
		self.assertEqual(response.status_code, 404)
		pass

	def test_update_case3(self):
		'''教师身份没写content'''
		client = Client()
		client.post('/login/', data={'id': "123456", 'password': "123456"});
		response = client.post('/user/' + str(self.c1pk) + '/homework/' + str(self.a1pk) + '/update/'
								, data = {});
		self.assertEqual(response.status_code, 404)
		
		pass

	def test_update_case4(self):
		'''合法操作'''
		client = Client()
		client.post('/login/', data={'id': "123456", 'password': "123456"});
		response = client.post('/user/' + str(self.c1pk) + '/homework/' + str(self.a1pk) + '/update/'
								, data = {'content': 'Too Young Too Simple, Sometimes Naive'});
		self.assertEqual(type(response), django.http.response.HttpResponseRedirect)
		
		try:
			assignment = Assignments.objects.get(pk=self.a1pk)
		except Assignments.DoesNotExist:
			assignment = None

		self.assertEqual((assignment is None), False)
		self.assertEqual(assignment.description, 'Too Young Too Simple, Sometimes Naive')   	
		
		pass

	def test_submit_case1(self):
		'''没登陆'''
		client = Client()
		response = client.post('/user/' + str(self.c1pk) + '/homework/' + str(self.a1pk) + '/submit/'
								, data = {});
		self.assertEqual(type(response), django.http.response.HttpResponseRedirect)
		pass

	def test_submit_case2(self):
		'''教师身份登陆'''
		client = Client()
		client.post('/login/', data={'id': "123456", 'password': "123456"});
		response = client.post('/user/' + str(self.c1pk) + '/homework/' + str(self.a1pk) + '/submit/'
								, data = {});
		self.assertEqual(response.status_code, 404)
		pass

	def test_submit_case3(self):
		'''忘记填写content'''
		client = Client()
		client.post('/login/', data={'id': "111111", 'password': "111111"});
		response = client.post('/user/' + str(self.c1pk) + '/homework/' + str(self.a1pk) + '/submit/'
								, data = {});
		self.assertEqual(response.status_code, 404)
		pass

	def test_submit_case4(self):
		'''没选这门课的人'''
		client = Client()
		client.post('/login/', data={'id': "111114", 'password': "111111"});
		response = client.post('/user/' + str(self.c1pk) + '/homework/' + str(self.a1pk) + '/submit/'
								, data = {'content': 'Wow Such Homework So Easy'});
		self.assertEqual(response.status_code, 404)
		pass

	def test_submit_case4(self):
		'''合法操作'''
		client = Client()
		client.post('/login/', data={'id': "111111", 'password': "111111"});
		response = client.post('/user/' + str(self.c1pk) + '/homework/' + str(self.a1pk) + '/submit/'
								, data = {'content': 'Wow Such Homework So Easy'});
		
		self.assertEqual(type(response), django.http.response.HttpResponseRedirect)
		
		try:
			submission = Submissions.objects.get(assignment_id=self.a1pk, student_id=self.s3pk)
		except Submissions.DoesNotExist:
			submission = None

		self.assertEqual((submission is None), False)
		self.assertEqual(submission.content, 'Wow Such Homework So Easy')   	
		
		pass

	def test_submission_case1(self):
		'''没登录'''
		client = Client()
		response = client.get('/user/' + str(self.c1pk) + '/homework/' + str(self.a1pk) + '/submission/' + str(self.sub1pk) + '/');
		self.assertEqual(type(response), django.http.response.HttpResponseRedirect)
		pass

	def test_submission_case2(self):
		'''没选这门课的人'''
		client = Client()
		client.post('/login/', data={'id': "111114", 'password': "111111"});
		response = client.get('/user/' + str(self.c1pk) + '/homework/' + str(self.a1pk) + '/submission/' + str(self.sub1pk) + '/');
		self.assertEqual(response.status_code, 404)
		pass

	def test_submission_case3(self):
		'''其他课的老师不能访问'''
		client = Client()
		client.post('/login/', data={'id': "123456", 'password': "123456"});
		response = client.get('/user/' + str(self.c1pk) + '/homework/' + str(self.a1pk) + '/submission/' + str(self.sub1pk) + '/');
		self.assertEqual(response.status_code, 404)
		pass

	def test_submission_case4(self):
		'''合法操作(学生)'''
		client = Client()
		client.post('/login/', data={'id': "111111", 'password': "111111"});
		response = client.get('/user/' + str(self.c1pk) + '/homework/' + str(self.a1pk) + '/submission/' + str(self.sub1pk) + '/');
		data = response.json()
		self.assertEqual(data.get('assignmentName'), "离散作业1")
		self.assertEqual(data.get('studentName'), "路人甲")
		self.assertEqual(data.get('content'), "群的定义是...")
		#self.assertEqual(data.get('submissionTime'), str(self.subtime))
		
		pass

	def test_submission_case5(self):
		'''合法操作(老师)'''
		client = Client()
		client.post('/login/', data={'id': "12345678", 'password': "12345678"});
		response = client.get('/user/' + str(self.c1pk) + '/homework/' + str(self.a1pk) + '/submission/' + str(self.sub1pk) + '/');
		data = response.json()
		self.assertEqual(data.get('assignmentName'), "离散作业1")
		self.assertEqual(data.get('studentName'), "路人甲")
		self.assertEqual(data.get('content'), "群的定义是...")
		#self.assertEqual(data.get('submissionTime'), str(self.subtime))
		
		pass



	def test_score_case1(self):
		'''没登录'''
		client = Client()
		response = client.post('/user/' + str(self.c1pk) + '/homework/' + str(self.a1pk) + '/submission/' + str(self.sub1pk) + '/score/',
							 data={'score': '0'})
		response = client.post('/user/' + str(self.c1pk) + '/homework/' + str(self.a1pk) + '/submission/' + str(self.sub1pk) + '/score/',
							 data={'score': '100'})
		self.assertEqual(type(response), django.http.response.HttpResponseRedirect)
		submission = Submissions.objects.get(pk=self.sub1pk)
		self.assertEqual((submission.score == 100), False);
		pass

	def test_score_case2(self):
		'''学生不能打分'''
		client = Client()
		client.post('/login/', data={'id': "111111", 'password': "111111"});
		response = client.get('/user/' + str(self.c1pk) + '/homework/' + str(self.a1pk) + '/submission/' + str(self.sub1pk) + '/score/');		
		self.assertEqual(response.status_code, 404)
		pass

#http://127.0.0.1:8000/user/1/homework/1/submission/2/score/
	##wrong teacher
	def test_score_case3(self):
		'''其他课的老师不能打分'''
		client = Client()
		client.post('/login/', data={'id': "123456", 'password': "123456"});
		response = client.get('/user/' + str(self.c1pk) + '/homework/' + str(self.a1pk) + '/submission/' + str(self.sub1pk) + '/score/');		
		self.assertEqual(response.status_code, 404)
		pass

	def test_score_case4(self):
		'''提交编号不存在'''
		client = Client()
		client.post('/login/', data={'id': "12345678", 'password': "12345678"});
		response = client.get('/user/' + str(self.c1pk) + '/homework/' + str(self.a1pk) + '/submission/' + '2147483647' + '/score/');		
		self.assertEqual(response.status_code, 404)
		pass

	def test_score_case5(self):
		'''提交不属于该课程'''
		client = Client()
		client.post('/login/', data={'id': "123456", 'password': "123456"});
		response = client.get('/user/' + str(self.c2pk) + '/homework/' + str(self.a1pk) + '/submission/' + str(self.sub1pk) + '/score/');		
		self.assertEqual(response.status_code, 404)
		pass

	def test_score_case6(self):
		'''忘记填写分数'''
		client = Client()
		client.post('/login/', data={'id': "12345678", 'password': "12345678"});
		response = client.post('/user/' + str(self.c1pk) + '/homework/' + str(self.a1pk) + '/submission/' + str(self.sub1pk) + '/score/',
							 data={})
		self.assertEqual(response.status_code, 404)
		pass

	def test_score_case7(self):
		'''分数不在范围内1'''
		client = Client()
		client.post('/login/', data={'id': "12345678", 'password': "12345678"});
		response = client.post('/user/' + str(self.c1pk) + '/homework/' + str(self.a1pk) + '/submission/' + str(self.sub1pk) + '/score/',
							 data={'score': '-1'})
		self.assertEqual(response.status_code, 404)
		pass

	# def test_score_case8(self):
	# 	'''分数不在范围内2'''
	# 	client = Client()
	# 	client.post('/login/', data={'id': "12345678", 'password': "12345678"});
	# 	response = client.post('/user/' + str(self.c1pk) + '/homework/' + str(self.a1pk) + '/submission/' + str(self.sub1pk) + '/score/',
	# 						 data={'score': '101'})
	# 	self.assertEqual(response.status_code, 404)
	# 	pass

	def test_score_case9(self):
		'''合法操作1'''
		client = Client()
		client.post('/login/', data={'id': "12345678", 'password': "12345678"});
		response = client.post('/user/' + str(self.c1pk) + '/homework/' + str(self.a1pk) + '/submission/' + str(self.sub1pk) + '/score/',
							 data={'score': '0'})
		response = client.post('/user/' + str(self.c1pk) + '/homework/' + str(self.a1pk) + '/submission/' + str(self.sub1pk) + '/score/',
							 data={'score': '100'})
		self.assertEqual(type(response), django.http.response.HttpResponseRedirect)
		submission = Submissions.objects.get(pk=self.sub1pk)
		self.assertEqual(submission.score, 100)
		pass

	# def test_score_case10(self):
	# 	'''合法操作2'''
	# 	client = Client()
	# 	client.post('/login/', data={'id': "12345678", 'password': "12345678"});
	# 	response = client.post('/user/' + str(self.c1pk) + '/homework/' + str(self.a1pk) + '/submission/' + str(self.sub1pk) + '/score/',
	# 						 data={'score': '100'})
	# 	response = client.post('/user/' + str(self.c1pk) + '/homework/' + str(self.a1pk) + '/submission/' + str(self.sub1pk) + '/score/',
	# 						 data={'score': '0'})
	# 	self.assertEqual(type(response), django.http.response.HttpResponseRedirect)
	# 	submission = Submissions.objects.get(pk=self.sub1pk)
	# 	self.assertEqual(submission.score, 0)
	# 	pass
