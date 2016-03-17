from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect

from .models import Device, SDN_Device  # , SDN_Port
from .forms import AddDeviceForm


class DeviceListView(ListView):
    model = Device
    template_name = 'devices/index_list_all.html'

    def get_context_data(self, **kwargs):
        ctx = super(DeviceListView, self).get_context_data(**kwargs)
        ctx['sdn'] = SDN_Device.objects.all()
        return ctx


class DeviceInfoView(DetailView):
    model = Device
    template_name = 'devices/index_legacy_detail.html'


class SDNInfoView(DetailView):
    model = SDN_Device
    template_name = 'devices/index_sdn_detail.html'
    """
    def get_context_data(self, **kwargs):
        ctx = super(SDNInfoView, self).get_context_data(**kwargs)
        dev = self.objects
        ctx['sdn_port'] = SDN_Port.objects.all()
    """


def base_page_view(request):
    return render(request, 'devices/index_general_info.html')


def topology_view(request):
    nodes = SDN_Device.objects.all()
    id_dict = dict()
    node_array = list()
    # link_array = list()
    ind = 0
    for dev in nodes:
        id_dict = {str(dev.id): ind}
        node_array.append('"id": ' + str(ind) + ', \
                      "name": "' + str(dev.hostname) + '", \
                      "icon": "../../static/img/switch.svg", \
                      "IpAddress": "' + str(dev.ip) + '", \
                      "ip_conn": "' + str(dev.ip_conn) + '", \
                      "port": ' + str(dev.port) + ', \
                      "hw_address": "' + str(dev.hw_address) + '", \
                      "company": "' + str(dev.company) + '", \
                      "device_type": "' + str(dev.device_type) + '", \
                      "protocol_vers": "' + str(dev.protocol_vers) + '", \
                      "serial": "' + str(dev.serial) + '"')
        ind += 1
    """
    for dev in nodes:
        link_array.append('"source": ' + str(id_dict[dev.id]) + ', \
                            "target": ' + str[id_dict[dev.id]] + '')


    node = ('"id": 0, "name": "YYYY", "icon": "../../static/img/switch.svg", \
             "IpAddress": "10.30.1.1"',
            '"id": 1, "name": "ZZZZ", "icon": "../../static/img/router.svg", \
            "IpAddress": "10.20.1.1"',
        '"id": 2, "name": "Router 2", "icon": "../../static/img/router.svg", \
            "IpAddress": "10.31.1.1"',
        '"id": 3, "name": "Switch 2", "icon": "../../static/img/switch.svg", \
            "IpAddress": "10.36.2.1"',
        '"id": 4, "name": "Switch 3", "icon": "../../static/img/switch.svg", \
            "IpAddress": "10.31.5.1"')

    link = ('"source": 1, "target": 2, "name": "A-B"',
            '"source": 1, "target": 6, "name": "A-C-1"',
            '"source": 1, "target": 6, "name": "A-C-2"',
            '"source": 2, "target": 6, "name": "A-F-2"')
    """
    link = ('"source": 1, "target": 2, "name": "A-B"',
            '"source": 1, "target": 2, "name": "A-C-1"',
            '"source": 0, "target": 1, "name": "A-C-1"',
            '"source": 0, "target": 2, "name": "A-C-1"')
    context = {'node': node_array, 'link': link, 'devices': nodes}
    return render(request, 'devices/index_topology.html', context)


def add_device(request):
    if request.method == "POST":
        form = AddDeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('devices:list')
    else:
        form = AddDeviceForm()
    return render(request, 'devices/base_device_add.html', {'form': form})


"""
def index(request):
    devices_list = Device.objects.order_by('id')[:10]
    context = {'devices_list': devices_list}
    return render(request, 'devices/index.html', context)
"""

"""
def detail(request, device_id):
    device = get_object_or_404(Device, pk=device_id)
    return render(request, 'devices/detail.html', {'device': device})
"""
