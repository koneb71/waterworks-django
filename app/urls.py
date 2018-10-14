
from django.conf.urls import url
from app.views import *

urlpatterns = [

    url(r'login/$', login_user, name='login_url'),
    url(r'logout/$', logout_user, name='logout_url'),
    url(r'page/client$', client_page, name='client-page'),
    url(r'client/$', client, name='client'),
    url(r'employee/$', employee, name='employee'),
    url(r'compute/$', compute_consumption, name='compute'),
    url(r'meter-reading/$', meter_reading, name='meter-reading'),
    url(r'transaction/meter$', client_transaction, name='transactions-client'),
    url(r'collections/$', collection, name='collections'),
    url(r'generate-report/$', generate_report, name='generate_report'),
    url(r'reports/$', reports, name='reports'),
    url(r'get-name/$', get_name, name='get_name'),
    url(r'', index, name='home'),

]