from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect

from .models import Device, SDN_Device
from .forms import AddDeviceForm


class DeviceListView(ListView):
    model = Device
    template_name = 'devices/base_device_list.html'


class SDNListView(ListView):
    model = SDN_Device
    template_name = 'devices/base_device_list.html'


class DeviceInfoView(DetailView):
    model = Device
    template_name = 'devices/base_device_detail.html'


class SDNInfoView(DetailView):
    model = SDN_Device
    template_name = 'devices/base_device_detail_sdn.html'


def base_page_view(request):
    return render(request, 'devices/base_general_info.html')


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
