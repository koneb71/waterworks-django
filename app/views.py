# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from app.models import *


def index(request):
    if request.user.is_authenticated():
        return render(request, 'app/home.html')
    else:
        return HttpResponseRedirect(reverse('login_url'))


def login_user(request):
    if request.method == 'POST':

        try:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return render(request, 'app/login.html', {'log_fail': True})

        except User.DoesNotExist:
            return render(request, 'app/login.html', {'log_fail': True})

    elif request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))

    return render(request, 'app/login.html', {'log_fail': False})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_url'))


def client(request):
    clients = Client.objects.all()
    return render(request, 'app/client.html', {'clients': clients})


def collection(request):
    if request.GET.get('employee'):
        collections = Collection.objects.filter(employee_id=request.GET.get('employee')).order_by('-id')
    else:
        collections = Collection.objects.all().order_by('-id')
    return render(request, 'app/transactions.html', {'collections': collections})


def employee(request):
    employees = Employee.objects.all().order_by('-id')
    return render(request, 'app/employee.html', {'employees': employees})


def meter_reading(request):
    clients = Client.objects.all()
    employees = Employee.objects.all()

    if request.method == 'POST':

        try:
            client = Client.objects.get(id=request.POST['client'])
            new_reading = request.POST['new_reading']
            last_reading = request.POST['last_reading']
            employee = Employee.objects.filter(id=request.POST['collector']).first()
            rate = WaterRate.objects.filter(name=request.POST['rate'], billing_classification_id=client.billing_classification.id).first()
            total_amount = request.POST['totalAmount']

            collect = Collection(
                client_id=client,
                employee_id=employee,
                encoder_id=request.user,
                water_rate=rate,
                last_read=int(last_reading),
                new_read=int(new_reading),
                total_amount=float(total_amount),
            )
            collect.save()

            return render(request, 'app/meter_reading.html', {'clients': clients, 'employees': employees, 'success': True})

        except Exception as e:
            print(e)
            return render(request, 'app/meter_reading.html', {'clients': clients, 'employees': employees, 'success': False})

    return render(request, 'app/meter_reading.html', {'clients': clients, 'employees': employees, 'success': False})


def compute_consumption(request):
    client_id = request.GET.get('client')
    new_reading = request.GET.get('new_reading')
    last_reading = request.GET.get('last_reading')
    if client_id:
        client = Client.objects.get(id=client_id)
        rates = WaterRate.objects.filter(billing_classification_id=client.billing_classification_id)
        last_read = 0
        collection = Collection.objects.filter(client_id=client_id)
        if collection.count() > 0:
            last_read = collection.order_by('-id')[0].new_read
        if client:
            diff = int(new_reading) - int(last_reading)
            for rate in rates:
                if rate.start <= diff <= rate.end:
                    if "minimum" in str(rate.name).lower(): compute = rate.rate
                    else: compute = diff * rate.rate
                    return JsonResponse({'status': 'success', 'rate': rate.name, 'amount': compute, 'last_read': last_read})

    return JsonResponse({'status': 'fail'})

