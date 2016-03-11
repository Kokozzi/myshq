from django.conf.urls import url
from devices.views import *

app_name = 'devices'
urlpatterns = [
    url(r'^$', base_page_view, name='base'),
    url(r'^add/$', add_device, name='add'),
    url(r'^list/$', DeviceListView.as_view(), name='list'),
    url(r'^list/(?P<pk>[0-9]+)/$', DeviceInfoView.as_view(), name='detail'),
]

# url(r'^$', views.index, name='index'),
# url(r'^(?P<device_id>[0-9]+)/$', views.detail, name='detail'),
