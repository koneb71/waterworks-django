import os

from celery.task import task

from app.ip1sms import SMSGateway
from app.models import *
from waterworks.settings import BASE_DIR

sms = SMSGateway()


@task
def announcement(message):
    sms.sendAll(message)


@task
def three_days_before_due_date():
    clients = Client.objects.all()
    today = datetime.date.today()

    for client in clients:
        latest_collection = Collection.objects.filter(client_id=client.id, is_paid=False)
        if latest_collection.count() > 0:
            latest_collection = latest_collection.order_by('-id')[0]
            due_date = latest_collection.due_date.date()
            diff = due_date - today
            if diff.days == 3:
                sms_template = open(os.path.join(BASE_DIR, 'app/sms_templates/3_days_left_notification.txt'),
                                    "r").read()
                sms_template = sms_template.format(bill=latest_collection.total_amount,
                                                   due_date=latest_collection.due_date.date().strftime('%B %d %Y'))
                sms.sendMessage(latest_collection.client_id.phone, sms_template)


@task
def one_day_before_due_date():
    clients = Client.objects.all()
    today = datetime.date.today()

    for client in clients:
        latest_collection = Collection.objects.filter(client_id=client.id, is_paid=False)
        if latest_collection.count() > 0:
            latest_collection = latest_collection.order_by('-id')[0]
            due_date = latest_collection.due_date.date()
            diff = due_date - today
            if diff.days == 1:
                sms_template = open(os.path.join(BASE_DIR, 'app/sms_templates/last_day_notification.txt'), "r").read()
                sms_template = sms_template.format(month=latest_collection.created_date.strftime('%B'),
                                                   bill=latest_collection.total_amount,
                                                   due_date=latest_collection.due_date.date().strftime('%B %d %Y'))
                sms.sendMessage(latest_collection.client_id.phone, sms_template)
