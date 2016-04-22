from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from subprocess import check_output, CalledProcessError
import json

from .models import Device
from .forms import AddDeviceForm


def Int2IP(ipnum):
    o1 = int(ipnum / 16777216) % 256
    o2 = int(ipnum / 65536) % 256
    o3 = int(ipnum / 256) % 256
    o4 = int(ipnum) % 256
    return '%(o4)s.%(o3)s.%(o2)s.%(o1)s' % locals()


def topology_generator():
    id_dict = dict()

    try:
        with open("/home/tsibulya/sdn/devices/topo_real.json") as json_file:
        # with open("/proc/marrow/dispatcher/topology") as json_file:
            json_data = json.load(json_file)
    except OSError:
            json_data = dict()
            json_data["nodes"] = 0
            return json_data

    try:
        with open("/home/tsibulya/sdn/devices/device_real2.json") as json_file2:
        # with open("/proc/vsms2_json_out") as json_file2:
            json_device = json.load(json_file2)
            json_device.pop('Links')
            data_flag = True
    except (OSError, ValueError):
            data_flag = False

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
                    if (len(str(link["P1"])) > 3):
                        temp_dict["port_src"] = Int2IP(link["P1"])
                    elif (link["P1"] == 0):
                        temp_dict["port_src"] = link["P1"]
                    else:
                        temp_dict["port_src"] = "Ethernet 1/0/" \
                                                + str(link["P1"])
                    if (len(str(link["P2"])) > 3):
                        temp_dict["port_dst"] = Int2IP(link["P2"])
                    elif (link["P2"] == 0):
                        temp_dict["port_dst"] = link["P2"]
                    else:
                        temp_dict["port_dst"] = "Ethernet 1/0/" \
                                                + str(link["P2"])
                    temp_dict["status"] = link["ST"]
                    temp_dict["Bandwidth"] = link["BW"]
                    temp_arr.append(temp_dict)
        node.pop('l')

    json_data.update({'links': temp_arr})

    ind = 0
    for node in json_data['nodes']:
        id_dict[node['id']] = ind
        node['id'] = ind
        if node['status'] == 1:
            if node['t'] == 1:
                node['icon'] = "../../../static/img/switch.svg"
                if (data_flag is True):
                    for sw in json_device["Switches"]:
                        if (str(sw['DatapathId']) == str(node["name"])):
                            node['DatapathId'] = sw['DatapathId']
                            node["name"] = sw["name"]
                            node["IpAddress"] = sw["IpAddress"]
                            node["ip_conn"] = sw["IpAddressConn"]
                            node["device_type"] = sw["TypeOfSwitch"]
                            node["protocol_vers"] = sw["ProtocolVersion"]
                            node["company"] = sw["CompanyName"]
                            node["port"] = sw["portNumber"]
                            node["hw_address"] = sw["hardwareAddress"]
                            node["serial"] = sw["SN"]
                            node["Ports"] = sw["Ports"]
            else:
                node['icon'] = "../../../static/img/router.svg"
                node['name'] = Int2IP(node['name'])
        else:
            if node['t'] == 1:
                node['icon'] = "../../../static/img/switch-d.svg"
            else:
                node['icon'] = "../../../static/img/router-d.svg"
                node['name'] = Int2IP(node['name'])
        ind += 1

    for link in json_data['links']:
        link_name = ""
        for node in json_data['nodes']:
            if ((data_flag is True) and (node["t"] == 1)):
                if (str(link['source']) == str(node['DatapathId'])):
                    link_name = node["name"]
                elif (str(link['target']) == str(node['DatapathId'])):
                    link_name = link_name + "-" + node["name"]
        link['name'] = link_name
        link['source'] = id_dict[link['source']]
        link['target'] = id_dict[link['target']]

    return json_data


class DeviceInfoView(DetailView):
    model = Device
    template_name = 'devices/index_legacy_detail.html'


def base_page_view(request):
    return render(request, 'devices/index_general_info.html')


def device_list_view(request):
    try:
        with open("/home/tsibulya/sdn/devices/device_real2.json") as sdn_file:
        # with open("/proc/vsms2_json_out") as sdn_file:
            json_sdn = json.load(sdn_file)
            json_sdn.pop('Links')
            sdn_opened = True
    except (OSError, ValueError):
            sdn = dict()
            sdn["nodes"] = "no data"
            sdn_opened = False

    if (sdn_opened is True):
        temp_arr = list()
        for sw in json_sdn["Switches"]:
            temp_dict = dict()
            temp_dict["status"] = 1
            temp_dict["device_type"] = sw["TypeOfSwitch"]
            temp_dict["hostname"] = sw["name"]
            temp_dict["ip"] = sw["IpAddress"]
            temp_dict["protocol_vers"] = sw["ProtocolVersion"]
            temp_dict["datapathid"] = sw["DatapathId"]
            temp_arr.append(temp_dict)
        sdn = dict()
        sdn.update({"Switches": temp_arr})

        legacy = Device.objects.all()

    return render(request, 'devices/index_list_all.html',
                  {'node_sdn': sdn, 'node_legacy': legacy})


def device_sdn_view(request, pk):
    try:
        with open("/home/tsibulya/sdn/devices/device_real2.json") as json_file:
        # with open("/proc/vsms2_json_out") as json_file:
            json_device = json.load(json_file)
            json_device.pop('Links')
    except (OSError, ValueError):
            json_device = dict()
            json_device["nodes"] = "no data"
            return render(request, 'devices/index_sdn_detail.html',
                          {'node': json_device})

    for sw in json_device["Switches"]:
        if (sw["DatapathId"] == pk):
            return render(request, 'devices/index_sdn_detail.html',
                          {'node': sw})
    raise Http404("No such sdn device!")


def device_legacy_view(request, pk):
    try:
        dev = Device.objects.get(ip=Int2IP(pk))
        return render(request, 'devices/index_list_all.html',
                      {'object': dev})
    except Device.DoesNotExist:
        raise Http404("No such device!")


def topology_view(request):
    return render(request, 'devices/index_topology.html',
                  {'node': topology_generator()})


@csrf_exempt
def service_add_view(request):
    if request.method == 'POST':
        try:
            with open("/home/tsibulya/sdn/devices/device_real2.json") as json_file:
            # with open("/proc/vsms2_json_out") as json_file:
                json_device = json.load(json_file)
                json_device.pop('Links')
        except (OSError, ValueError):
            return HttpResponse('fail')
        name = request.POST['name']
        count = int(request.POST["count"])
        pe = list()
        i = 0
        while (i < count):
            node = dict()
            for sw in json_device["Switches"]:
                if (str(request.POST['nodes[' + str(i) + '][name]']) == str(sw["name"])):
                    node["id"] = sw["DatapathId"]
            node["physical"] = request.POST['nodes[' + str(i) + '][physical]']
            node["physical"] = str(node["physical"]).split("/")[2]
            node["ip"] = request.POST['nodes[' + str(i) + '][ip]']
            node["port"] = request.POST['nodes[' + str(i) + '][port]']
            pe.append(node)
            i += 1

        # assert False, request.POST

        i = 0
        modulus = len(pe)
        command = list()
        while (i < modulus):
            text = "apply_tunnel_route:"
            text += name + "--" + str(i + 1) + "/" + name + "--" + str(i + 1) + ":"
            text += str(pe[i % modulus]["id"]) + ":"
            text += str(pe[i % modulus]["physical"]) + ":"
            text += str(pe[(i + 1) % modulus]["id"]) + ":"
            text += str(pe[(i + 1) % modulus]["physical"]) + ":"
            command.append(text)
            i += 1

        service_dict = dict()
        service_dict["name"] = name
        service_dict.update({'nodes': pe})
        service_dict["bw"] = request.POST['bw']

        tunnels_array = list()
        i = 0
        while i < modulus:
            tun_dict = dict()
            tun_dict["tun_name"] = name + "--" + str(i + 1)
            tun_dict["path_name"] = tun_dict["tun_name"]
            tun_dict["src"] = str(pe[i % modulus]["id"])
            tun_dict["src_port"] = str(pe[i % modulus]["physical"])
            tun_dict["dst"] = str(pe[(i + 1) % modulus]["id"])
            tun_dict["dst_port"] = str(pe[(i + 1) % modulus]["physical"])
            tunnels_array.append(tun_dict)
            i += 1

        service_dict.update({'tunnels': tunnels_array})

        # i = 0
        # for cmd in command:
        #     try:
        #         result = json.loads(check_output(['python', '/root/projects/marrow/python-marrow/test.py', '33', cmd]).decode('utf-8'))
        #     except CalledProcessError:
        #         try:
        #             result = json.loads(check_output(['python', '/root/projects/marrow/python-marrow/test.py', '33', cmd]).decode('utf-8'))
        #         except CalledProcessError:
        #             return HttpResponse('path_fail')
        #     path = ""
        #     for elem in result["path"]:
        #         path += str(elem) + "-"
        #     tunnels_array[i]["path"] = path
        #     i += 1

        with open('/home/tsibulya/sdn/devices/services.json', 'r+') as services_json:
        # with open('/var/www/sdn/devices/services.json', 'r+') as services_json:
            services = json.load(services_json)
            services["services"].append(service_dict)
            services_json.seek(0)
            json.dump(services, services_json, indent=4)

        # band = request.POST['bw']
        # req_nodes = request.POST.getlist('req_nodes')
        # req_links = request.POST.getlist('req_links')
        response = dict()
        response["text"] = "success"
        response["name"] = name
        return JsonResponse(response)
    return render(request, 'devices/index_service_add.html',
                  {'node': topology_generator()})


def service_detail_view(request, pk):
    with open('/home/tsibulya/sdn/devices/services.json') as services_json:
        services = json.load(services_json)
        for serv in services["services"]:
            if (serv["name"] == pk):
                path_arr = str(serv["tunnels"][0]["path"]).split('-')
                path_arr.pop()
                path = ""
                for elem in path_arr:
                    path += str(elem) + "-"
                return render(request, 'devices/index_service_detail.html',
                              {'node': topology_generator(), 'service': serv,
                               'path': path})
    raise Http404("No such service!")


def service_list_view(request):
    return render(request, 'devices/index_sdn_detail.html')


def add_device(request):
    if request.method == "POST":
        form = AddDeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('devices:list')
    else:
        form = AddDeviceForm()
    return render(request, 'devices/base_device_add.html', {'form': form})
