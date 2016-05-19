from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

# Create your views here.

def login(request):
    return HttpResponseRedirect(reverse("welcome"))

def welcome(request):
    return HttpResponse("Hello user A!")

