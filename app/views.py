# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from app.ip1sms import SMSGateway
from app.models import *


def index(request):
    if request.user.is_authenticated():
        num_clients = Client.objects.all().count()
        num_paid_collections = Collection.objects.filter(is_paid=True).count()
        num_employees = Employee.objects.all().count()
        return render(request, 'app/home.html', {'num_clients': num_clients, "num_paid_collections": num_paid_collections,
                                                 "num_employees": num_employees})
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


def client_page(request):
    return render(request, 'client/index.html')


def client(request):
    clients = Client.objects.all()
    return render(request, 'app/client.html', {'clients': clients})


def collection(request):
    if request.GET.get('employee'):
        collections = Collection.objects.filter(employee_id=request.GET.get('employee')).order_by('-id')
    elif request.GET.get('client'):
        collections = Collection.objects.filter(client_id=request.GET.get('client')).order_by('-id')
    else:
        collections = Collection.objects.all().order_by('-id')
    return render(request, 'app/transactions.html', {'collections': collections})


def employee(request):
    employees = Employee.objects.all().order_by('-id')
    return render(request, 'app/employee.html', {'employees': employees})


def meter_reading(request):
    sms = SMSGateway(from_name="WaterWorks")
    clients = Client.objects.all()
    employees = Employee.objects.all()

    if request.method == 'POST':

        try:
            client = Client.objects.get(id=request.POST['client'])
            new_reading = request.POST['new_reading']
            last_reading = request.POST['last_reading']
            employee = Employee.objects.filter(id=request.POST['collector']).first()
            rate = WaterRate.objects.filter(name=request.POST['rate'],
                                            billing_classification_id=client.billing_classification.id).first()
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

            sms_template = open("app/sms_templates/after_read_notification.txt", "r").read()
            sms_template = sms_template.format(month=collect.created_date.strftime("%B"), bill=collect.total_amount,
                                               due_date=collect.due_date.date().strftime('%B %d %Y'))
            sms.sendMessage(collect.client_id.phone, sms_template)

            return render(request, 'app/meter_reading.html',
                          {'clients': clients, 'employees': employees, 'success': True})

        except Exception as e:
            print(e)
            return render(request, 'app/meter_reading.html',
                          {'clients': clients, 'employees': employees, 'success': False})

    return render(request, 'app/meter_reading.html', {'clients': clients, 'employees': employees, 'success': False})


def compute_consumption(request):
    client_id = request.GET.get('client')
    new_reading = request.GET.get('new_reading')
    last_reading = request.GET.get('last_reading')
    if new_reading == 0 == last_reading:
        collection = Collection.objects.filter(client_id=client_id)
        if collection.count() > 0:
            last_reading = collection.order_by('-id')[0].new_read
            return JsonResponse(
                {'status': 'success', 'consumption': 0, 'amount': 0, 'last_read': last_reading})
    elif client_id:
        client = Client.objects.get(id=client_id)
        rates = WaterRate.objects.filter(billing_classification_id=client.billing_classification_id)
        collection = Collection.objects.filter(client_id=client_id)

        if collection.count() > 0:
            last_reading = collection.order_by('-id')[0].new_read
        if client:
            diff = int(new_reading) - int(last_reading)
            counter = 1
            total_amount = 0.0
            for rate in rates:
                if "minimum" in str(rate.name).lower():
                    total_amount += float(rate.rate)
                    counter += 10
                elif rate.start <= diff <= rate.end and "above" in str(rate.name).lower():
                    while counter < diff and (diff - counter) > 9:
                        total_amount += float(rate.rate * 10)
                        counter += 10
                    if (diff - counter) < 9:
                        remaining = diff - counter + 1
                        if remaining > 0:
                            total_amount += float(remaining * rate.rate)
                elif rate.start <= diff <= rate.end:
                    if (diff - counter) < 9:
                        remaining = diff - counter + 1
                        if remaining > 0:
                            total_amount += float(remaining * rate.rate)
                    else:
                        total_amount += float(10 * rate.rate)
                        counter += 10
            return JsonResponse(
                        {'status': 'success', 'consumption': diff, 'amount': str(total_amount), 'last_read': last_reading})

    return JsonResponse({'status': 'fail'})


def client_transaction(request):
    client_id = request.GET.get('id')
    if client_id:
        client = Collection.objects.filter(client_id__meter_serial_number=client_id)
        transactions = []
        for cl in client:
            transactions.append(
                {'name': "%s, %s" % (cl.client_id.last_name, cl.client_id.first_name),
                 'class': cl.client_id.billing_classification.name, 'last_read': cl.last_read, 'new_read': cl.new_read,
                 'amount': cl.total_amount, 'created_date': cl.created_date.date(), 'due_date': cl.due_date.date(), 'is_paid': cl.is_paid}
            )
        return JsonResponse({'data': transactions})
    return JsonResponse({'data': []})
