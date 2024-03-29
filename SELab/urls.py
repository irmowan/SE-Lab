"""SELab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
import user.views, course.views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="user/homepage.html"), name='homepage'),
    url(r'^login/$', user.views.login),
    url(r'^logout/$', user.views.logout),
    url(r'^user/$', user.views.welcome, name="welcome"),
    url(r'^user/(?P<course_id>\d+)/$', course.views.index),
    url(r'^user/(?P<course_id>\d+)/homework/', include("homework.urls")),
    url(r'^admin/', admin.site.urls),
]
