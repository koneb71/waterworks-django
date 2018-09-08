
from django.conf.urls import url
from app.views import *

urlpatterns = [

    url(r'login/$', login_user, name='login_url'),
    url(r'logout/$', logout_user, name='logout_url'),
    url(r'client/$', client, name='client'),
    url(r'compute/$', compute_consumption, name='compute'),
    url(r'meter-reading/$', meter_reading, name='meter-reading'),
    url(r'collections/$', collection, name='collections'),
    url(r'', index, name='home'),

]