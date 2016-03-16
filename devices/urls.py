from django.conf.urls import url
from devices.views import *

app_name = 'devices'
urlpatterns = [
    url(r'^$', base_page_view, name='base'),
    url(r'^topology/$', topology_view, name='topology'),
    url(r'^add/$', add_device, name='add'),
    url(r'^list/$', DeviceListView.as_view(), name='device_list'),
    url(r'^legacy_detail/(?P<pk>[0-9]+)/$',
        DeviceInfoView.as_view(), name='legacy_detail'),
    url(r'^sdn_detail/(?P<pk>[0-9]+)/$',
        SDNInfoView.as_view(), name='sdn_detail'),
]

# url(r'^$', views.index, name='index'),
# url(r'^(?P<device_id>[0-9]+)/$', views.detail, name='detail'),
