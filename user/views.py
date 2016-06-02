from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.

def login(request):
    user = auth.authenticate(id=request.POST.get('id'), password=request.POST.get('password'))
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse("welcome"))
        else:
            return HttpResponse("Fail: a disabled account")
    else:
        return HttpResponse("Login fail!")

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("homepage"))

@login_required
def welcome(request):
    data = {"name": request.user.name, "email": request.user.email}
    return HttpResponse(str(data))

