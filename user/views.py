from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.

def login(request):
    user = auth.authenticate(id="13307130319", password="qwerty")
    #user = auth.authenticate(id=request.POST['id'], password=request.POST['password'])
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse("welcome"))
        else:
            return HttpResponse("Fail: a disabled account")
    else:
        return HttpResponse("Login fail!")

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("homepage"))

@login_required
def welcome(request):
    return HttpResponse("Hello {}!".format(request.user.name))

