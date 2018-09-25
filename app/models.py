import datetime
import random
import time
import django
from dateutil.relativedelta import relativedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


# CUSTOM USER AUTH
###############################################################################

class UserManager(BaseUserManager):
    def create_user(self, password, **kwargs):
        user = self.model(
            is_active=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **kwargs):
        user = self.model(
            username=username,
            is_superuser=True,
            is_staff=True,
            is_active=True,
            is_admin=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return UserManager


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'username'

    username = models.CharField(unique=True, max_length=30, null=True, blank=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    middle_name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_accountant = models.BooleanField(default=False, verbose_name="Accountant")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False, verbose_name="Admin")
    created_date = models.DateTimeField(default=datetime.datetime.now, blank=True)

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.first_name

    objects = UserManager()


###############################################################################
###############################################################################
###############################################################################

def randN(n):
    l = list(range(10))  # compat py2 & py3
    while l[0] == 0:
        random.shuffle(l)
    return ''.join(str(d) for d in l[:n])


class BillingClassification(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)
    created_date = models.DateTimeField(default=datetime.datetime.now, blank=True)

    def __str__(self):
        return self.name


class BlockArea(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)
    created_date = models.DateTimeField(default=datetime.datetime.now, blank=True)

    def __str__(self):
        return self.name


class Client(models.Model):
    account_number = models.CharField(default=time.strftime("%Y%d%M%S", time.gmtime()), max_length=30)
    meter_serial_number = models.CharField(max_length=30, default=randN(9))
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    middle_name = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    billing_classification = models.ForeignKey(BillingClassification)
    block_area = models.ForeignKey(BlockArea)
    street_address1 = models.CharField(max_length=30, null=True, blank=True)
    street_address2 = models.CharField(max_length=30, null=True, blank=True)
    barangay = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    postalCode = models.CharField(max_length=30, null=True, blank=True)
    created_date = models.DateTimeField(default=datetime.datetime.now, blank=True)

    def __str__(self):
        return "%s, %s %s," % (self.last_name, self.first_name, self.middle_name)


class ClientProxy(Client):
    class Meta:
        proxy = True
        verbose_name = 'SMS Announcement'


class Employee(models.Model):
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    block_area = models.ManyToManyField(BlockArea)
    created_date = models.DateTimeField(default=datetime.datetime.now, blank=True)

    class Meta:
        verbose_name = 'Collector'
        verbose_name_plural = 'Collectors'

    def __str__(self):
        return "%s, %s" % (self.last_name, self.first_name)


class WaterRate(models.Model):
    billing_classification_id = models.ForeignKey(BillingClassification)
    name = models.CharField(max_length=30, null=True, blank=True)
    start = models.IntegerField(default=0)
    end = models.IntegerField(default=0)
    rate = models.FloatField(default=0.0, null=True, blank=True)
    created_date = models.DateTimeField(default=datetime.datetime.now, blank=True)

    def __str__(self):
        return "%s - %s" % (self.billing_classification_id.name, self.name)


class Collection(models.Model):
    client_id = models.ForeignKey(Client)
    encoder_id = models.ForeignKey(User)
    employee_id = models.ForeignKey(Employee)
    water_rate = models.ForeignKey(WaterRate, null=True, blank=True)
    last_read = models.IntegerField(default=0, null=True, blank=True)
    new_read = models.IntegerField(default=0, null=True, blank=True)
    total_amount = models.FloatField(default=0, null=True, blank=True)
    created_date = models.DateTimeField(default=datetime.datetime.today(), blank=True)
    due_date = models.DateTimeField(default=datetime.datetime.today() + relativedelta(months=1), blank=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return "%s, %s %s," % (self.client_id.last_name, self.client_id.first_name, self.client_id.middle_name)

    def get_total_consumption(self):
        return self.new_read - self.last_read


class Configuration(models.Model):
    surcharge_days = models.IntegerField(default=20)
    surcharge_fee = models.FloatField(default=(14 / 100))
    discount = models.FloatField(default=(5 / 100))
    grace_period = models.IntegerField(default=5)
    disconnection_months = models.IntegerField(default=3)
