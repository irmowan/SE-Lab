from django.conf.urls import url
from . import views

app_name = 'homework'
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^new/$', views.new),
    url(r'^new/create/$', views.create),
    url(r'^delete/$', views.delete),
    url(r'^(?P<assignment_id>\d+)/$', views.detail, name="detail"),
    url(r'^(?P<assignment_id>\d+)/update/$', views.update),
    url(r'^(?P<assignment_id>\d+)/submit/$', views.submit),
    url(r'^(?P<assignment_id>\d+)/submission/(?P<submission_id>\d+)/$', views.submission, name="submission"),
    url(r'^(?P<assignment_id>\d+)/submission/(?P<submission_id>\d+)/score/$', views.score),
]

