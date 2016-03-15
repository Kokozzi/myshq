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
