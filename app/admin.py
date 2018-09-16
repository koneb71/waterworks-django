# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django import forms
from rangefilter.filter import DateRangeFilter

from app.models import *
from app.resource import CollectionResource

admin.site.site_header = "WATERWORKS ADMINISTRATION"
admin.site.site_title = "WaterWorks Admin Portal"
admin.site.index_title = "WaterWorks Admin"

UserAdmin.list_display += (
'first_name', 'last_name', 'middle_name', 'email', 'phone', 'is_staff', 'is_accountant', 'is_active', 'is_admin',
'created_date',)


class UserCreationFormExtended(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationFormExtended, self).__init__(*args, **kwargs)
        self.fields['email'] = forms.EmailField(label=("E-mail"), max_length=75)
        # self.fields['password'] = forms.CharField(max_length=32, widget=forms.PasswordInput())


UserAdmin.add_form = UserCreationFormExtended
UserAdmin.add_fieldsets += ((None, {
    'fields': (
    'first_name', 'last_name', 'middle_name', 'email', 'phone', 'is_staff', 'is_accountant', 'is_active', 'is_admin',
    'created_date',)
}),)


@admin.register(User)
class UsersAdmin(UserAdmin):
    pass


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name', 'meter_serial_number', "account_number", "billing_classification__name",
                     'block_area__name')
    list_display = ("account_number", "meter_serial_number", "first_name", "middle_name", "last_name", "phone",
                    "billing_classification", "block_area")


@admin.register(BlockArea)
class BlockAreaAdmin(admin.ModelAdmin):
    pass


@admin.register(BillingClassification)
class BillingClassificationAdmin(admin.ModelAdmin):
    pass


@admin.register(WaterRate)
class WaterRateAdmin(admin.ModelAdmin):
    list_display = ("billing_classification_id", "name", "start", "end", "rate")


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ("surcharge_days", "surcharge_fee", "discount_display", "grace_period", "disconnection_months")

    def discount_display(self, obj):
        return '%s%%' % obj.discount


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'get_block_areas')

    def get_block_areas(self, obj):
        return ", ".join([b.name for b in obj.block_area.all()])


@admin.register(Collection)
class CollectionsAdmin(ImportExportModelAdmin):
    resource_class = CollectionResource

    list_filter = (
        ('created_date', DateRangeFilter),
    )
    search_fields = ("client_id__name", "water_rate__name")
    list_display = (
    "client_id", "water_rate", "last_read", "new_read", "total_amount", "created_date", "due_date", "is_paid")
