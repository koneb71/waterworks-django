# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django import forms

from app.models import *

admin.site.site_header = "WATERWORKS ADMINISTRATION"
admin.site.site_title = "WaterWorks Admin Portal"
admin.site.index_title = "WaterWorks Admin"

UserAdmin.list_display += ('first_name', 'last_name', 'middle_name', 'email', 'phone', 'is_staff', 'is_accountant', 'is_active', 'is_admin', 'created_date',)

class UserCreationFormExtended(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationFormExtended, self).__init__(*args, **kwargs)
        self.fields['email'] = forms.EmailField(label=("E-mail"), max_length=75)
        #self.fields['password'] = forms.CharField(max_length=32, widget=forms.PasswordInput())

UserAdmin.add_form = UserCreationFormExtended
UserAdmin.add_fieldsets += ((None, {
        'fields': ('first_name', 'last_name', 'middle_name', 'email', 'phone', 'is_staff', 'is_accountant', 'is_active', 'is_admin',
'created_date',)
    }),)

@admin.register(User)
class UsersAdmin(UserAdmin):
    pass


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(BlockArea)
class BlockAreaAdmin(admin.ModelAdmin):
    pass


@admin.register(BillingClassification)
class BillingClassificationAdmin(admin.ModelAdmin):
    pass


@admin.register(WaterRate)
class WaterRateAdmin(admin.ModelAdmin):
    pass


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    pass


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass


@admin.register(Collection)
class CollectionsAdmin(admin.ModelAdmin):
    pass
