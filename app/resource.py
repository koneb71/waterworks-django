from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from .models import *


class CollectionResource(resources.ModelResource):
    account_number = fields.Field(
        column_name='Account Number',
        attribute='client_id',
        widget=ForeignKeyWidget(Client, 'account_number'))

    meter_serial_number = fields.Field(
        column_name='Meter Serial Number',
        attribute='client_id',
        widget=ForeignKeyWidget(Client, 'meter_serial_number'))

    class Meta:
        model = Collection
        fields = ('id', 'account_number', 'meter_serial_number', 'due_date', 'total_amount', 'is_paid')
        export_order = ('id', 'account_number', 'meter_serial_number', 'due_date', 'total_amount', 'is_paid')

        widgets = {
            'due_date': {'format': '%d.%m.%Y'},
        }