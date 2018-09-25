# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from admin_interface.models import Theme
from django.contrib import admin
from django.contrib.auth.models import Group
from django_celery_beat.models import SolarSchedule
from django_celery_results.models import TaskResult
from tasks import announcement
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django import forms
from rangefilter.filter import DateRangeFilter

from app.forms import SMSAnnouncementForm
from app.ip1sms import SMSGateway
from app.models import *
from app.resource import CollectionResource

admin.site.site_header = "WATERWORKS ADMINISTRATION"
admin.site.site_title = "WaterWorks Admin Portal"
admin.site.index_title = "WaterWorks Admin"


class ReadOnlyAdmin(admin.ModelAdmin):
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields] + \
               [field.name for field in obj._meta.many_to_many]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class UserCreationFormExtended(UserCreationForm):
    def __init__(self, *args, **kwargs):
        position = (
            ('Admin', 'Admin'),
            ('Accountant', 'Accountant'),

        )
        super(UserCreationFormExtended, self).__init__(*args, **kwargs)
        self.fields['email'] = forms.EmailField(label=("E-mail"), max_length=75)
        self.fields['position'] = forms.Select(choices=position)


UserAdmin.add_form = UserCreationFormExtended
UserAdmin.add_fieldsets += ((None, {
    'fields': (
        'first_name', 'last_name', 'middle_name', 'email', 'phone',
        'created_date',)
}),)


@admin.register(User)
class UsersAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'middle_name', 'position', 'phone',
        'created_date',)
    list_filter = ('is_accountant', 'is_admin',)

    def position(self, obj):
        pos = []
        if obj.is_accountant:
            pos.append('Accountant')
        if obj.is_admin:
            pos.append('Admin')
        return ', '.join(pos)


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
    list_display = ('first_name', 'last_name', 'block_areas')

    def block_areas(self, obj):
        return ", ".join([b.name for b in obj.block_area.all()])


@admin.register(Collection)
class CollectionsAdmin(ImportExportModelAdmin):
    resource_class = CollectionResource

    list_filter = (
        ('created_date', DateRangeFilter),
    )
    search_fields = ("client_id__name",)
    list_display = (
        "client_id", "last_read", "new_read", "total_amount", "created_date", "due_date", "is_paid")


sms = SMSGateway()


class SMSAnnouncementAdmin(admin.ModelAdmin):
    actions = None
    list_display_links = None
    form = SMSAnnouncementForm
    fieldsets = (
        ('Announcement', {
            'fields': ('message',)}),)

    def save_model(self, request, obj, form, change):
        announcement.delay(request.POST['message'])


admin.site.register(ClientProxy, SMSAnnouncementAdmin)
admin.site.unregister(Group)
admin.site.unregister(SolarSchedule)
admin.site.unregister(TaskResult)
admin.site.unregister(Theme)
