# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from .forms import *
import  numpy as np
import json
from django.core import serializers
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder


#EXCEPTIONS WERE JUST RAISED, THEY CAN BE HANDLED DIFFERENTLY USING AJAX OR OTHER HTTP RESPONSES. for now i left them as they are


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email =  userObj['email']
            password =  userObj['password']

            if not (len(User.objects.filter(username=username))!=0 or len(User.objects.filter(email=email))!= 0):
                User.objects.create_user(username, email, password)
                user = authenticate(username = username, password = password)
                login(request, user)
                request.session['member_id'] = user.id
                request.session['username'] = user.username

                return HttpResponseRedirect('/')
            else:

                raise forms.ValidationError('Looks like a username with that email or password already exists')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form' : form})


def loggingout(request):
    try:
        del request.session['member_id']
        del request.session['username']
        logout(request)

    except KeyError:
        pass
    context = {'foo': 'bar'}

    return render(request, 'logedout.html', context)


def loginngin(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            password = userObj['password']

            if not (len(User.objects.filter(username=username)) == 0):
                user = authenticate(username=username, password=password)
                if user is not None:

                    login(request, user)
                    request.session['member_id'] = user.id
                    request.session['username'] = user.username
                    return HttpResponseRedirect('/')
                else:
                    raise forms.ValidationError("username or password is not correct")
            else:

                raise forms.ValidationError('this username does not exist')
    else:
        form = UserRegistrationForm()
    return render(request, 'login.html', {'form': form})


def add_vacation(request):
    if request.method == "POST":
        form = AddVacation(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            start_date = userObj['start_date']
            end_date = userObj['end_date']
            description = userObj['description']
            username = request.session['username']
            user = User.objects.filter(username = username).get()
            id = len(Vacation.objects.filter(employee = user))+1        #number of vacations per user
            duration = np.busday_count(start_date, end_date)
            if (duration <=0):
                raise forms.validationError("the vacation is for less than one day")
            else:
                v = Vacation(idd = id,employee = user, start_date= str(start_date), end_date = str(end_date),description=description, total_period=duration)
                v.save()

    else:
        form = AddVacation()
    return render(request, 'vacation_added.html', {'form': form})



class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        try:
            username = request.session['username']
            user = User.objects.filter(username=username).get()
            vacations = Vacation.objects.filter(employee=user).values('start_date', 'end_date', 'total_period','description', 'idd')
            data = json.dumps(list(vacations), cls=DjangoJSONEncoder)
            context = {"obj_as_json": data}
        except:
            context = {'foo':'boo'}

        return render(request, 'home.html', context)



@csrf_exempt
def updateVacation(request):
    if request.is_ajax():
        start_date = request.POST.get('start_date')
        end_date =(request.POST.get('end_date'))
        description = request.POST.get('description')
        duration = np.busday_count(start_date, end_date)
        if(np.busday_count(end_date, datetime.date.today())<=0):
            raise forms.validationError("you can't edit old vacations")

        if (duration<=0):
            raise forms.validationError("the vacation is for less than one day")

        else:
            idd = request.POST.get('idd')
            username = request.session['username']
            user = User.objects.filter(username=username).get()
            vacation = Vacation.objects.filter(employee = user, idd =idd).update(start_date=start_date, end_date=end_date, description = description, total_period=duration)
            return HttpResponse("success")
