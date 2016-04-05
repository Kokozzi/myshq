from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
import json

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
    id_dict = dict()

    with open("/home/tsibulya/sdn/devices/topo_real.json") as json_file:
        json_data = json.load(json_file)

    temp_arr = list()

    for node in json_data["nodes"]:
        node["name"] = node["id"]
        node["status"] = 1
        for link in node['l']:
            if link["t"] == "U":
                add = True
                for element in temp_arr:
                    if (element["source"] == link["N"] and
                       element["target"] == node["id"]):
                            add = False
                if add:
                    temp_dict = dict()
                    temp_dict["source"] = node["id"]
                    temp_dict["target"] = link["N"]
                    temp_dict["port_src"] = link["P1"]
                    temp_dict["port_dst"] = link["P2"]
                    temp_dict["status"] = link["ST"]
                    temp_dict["Bandwidth"] = link["BW"]
                    temp_arr.append(temp_dict)
        node.pop('l')

    json_data.update({'links': temp_arr})

    ind = 0
    for nodes in json_data['nodes']:
        id_dict[nodes['id']] = ind
        nodes['id'] = ind
        if nodes['status'] == 1:
            nodes['icon'] = "../../static/img/switch.svg"
        else:
            nodes['icon'] = "../../static/img/switch-d.svg"
        ind += 1

    for link in json_data['links']:
        link['source'] = id_dict[link['source']]
        link['target'] = id_dict[link['target']]

    # context = {'node': json_data, 'devices': nodes}
    return render(request, 'devices/index_topology.html', {'node': json_data})


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
