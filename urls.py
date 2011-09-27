from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from motorfleet.views import *

urlpatterns = patterns('',
    (r'^welcome/$', direct_to_template, {'template': 'motorfleet/welcome.html'}),
    url(r'^fleet/(?P<fleet_id>\d+)/$', fleet, name='fleet'),
    url(r'^editfleet/(?P<fleet_id>\d+)/$', editfleet, name='editfleet'),
    url(r'^personaldetails/(?P<user_id>\d+)/$', personaldetails, name='personaldetails'),
    url(r'^drivinghistory/(?P<user_id>\d+)/$', drivinghistory, name='drivinghistory'),
    url(r'^addvehicles/(?P<sharedexpense_id>\d+)/(?P<user_id>\d+)/$', addvehicles, name='addvehicles'),
    url(r'^addclaims/(?P<sharedexpense_id>\d+)/(?P<user_id>\d+)/$', addclaims, name='addclaims'),
)

