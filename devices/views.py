from django.views.generic.detail import DetailView
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from subprocess import check_output, CalledProcessError
import json

from .models import Device

# assert False, request.POST


def Int2IP(ipnum):
    o1 = int(ipnum / 16777216) % 256
    o2 = int(ipnum / 65536) % 256
    o3 = int(ipnum / 256) % 256
    o4 = int(ipnum) % 256
    return '%(o4)s.%(o3)s.%(o2)s.%(o1)s' % locals()


def get_topo_local():
    try:
        with open("/home/tsibulya/sdn/devices/topo_real.json") as topo_file:
            topology = json.load(topo_file)
    except OSError:
        topology = dict()
        topology["nodes"] = 0
    return topology


def get_topo_prod():
    p = "python"
    path = "/root/projects/marrow/modules-uspace/marrow.py"
    cmd = "topology"
    try:
        topology = json.loads(check_output([p, path, cmd]).decode('utf-8'))
    except CalledProcessError:
        topology = dict()
        topology["nodes"] = 0
    return topology


def get_of_local():
    try:
        with open("/home/tsibulya/sdn/devices/device_real3.json") as js:
            of_device = json.load(js)
    except (OSError, ValueError):
        of_device = dict()
        of_device["Switches"] = "no data"
    return of_device


def get_of_prod():
    try:
        with open("/proc/vsms2_json_out") as js:
            of_device = json.load(js)
    except (OSError, ValueError):
        of_device = dict()
        of_device["Switches"] = "no data"
    return of_device


def get_services_local():
    try:
        with open('/home/tsibulya/sdn/devices/services_real.json') as js:
            services = json.load(js)
    except (OSError, ValueError):
        services = dict()
        services["tunnels"] = "no data"
    return services


def get_services_prod():
    p = "python"
    path = "/root/projects/marrow/modules-uspace/marrow.py"
    cmd = "tunnels"
    try:
        services = json.loads(check_output([p, path, cmd]).decode('utf-8'))
    except CalledProcessError:
        services = dict()
        services["tunnels"] = "no data"
    return services


def topology_generator():
    ##
    json_data = get_topo_local()
    # json_data = get_topo_prod()
    if (json_data["nodes"] == 0):
        return json_data
    ##
    json_device = get_of_local()
    # json_device = get_of_prod()
    if (json_device["Switches"] == "no data"):
        data_flag = False
    else:
        data_flag = True

    id_dict = dict()
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
                node['DatapathId'] = node['name']
                node['IpAddress'] = Int2IP(node['name'])

                legacy = Device.objects.get(cust_ip=node['IpAddress'])
                node['name'] = legacy.hostname
                node['device_type'] = legacy.hardware
                node['company'] = legacy.icon
                node['serial'] = legacy.serial
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
            if (str(link['source']) == str(node['DatapathId'])):
                link_name = node["name"] + link_name
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
    ##
    json_sdn = get_of_local()
    # json_sdn = get_of_prod()
    if (json_sdn["Switches"] == "no data"):
        sdn_opened = False
    else:
        sdn_opened = True

    legacy = Device.objects.all()

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
        return render(request, 'devices/index_list_all.html',
                      {'node_sdn': sdn, 'node_legacy': legacy})
    else:
        return render(request, 'devices/index_list_all.html',
                      {'node_legacy': legacy})


def device_sdn_view(request, pk):
    ##
    json_sdn = get_of_local()
    # json_sdn = get_of_prod()
    if (json_sdn["Switches"] == "no data"):
        return render(request, 'devices/index_sdn_detail.html',
                      {'node': json_sdn})
    else:
        for sw in json_sdn["Switches"]:
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
        ##
        json_device = get_of_local()
        # json_device = get_of_prod()
        if (json_device["Switches"] == "no data"):
            return HttpResponse('fail')

        p = "python"
        path = "/root/projects/marrow/modules-uspace/marrow.py"
        cmd = "create-tunnel"
        src = "-S="
        dst = "-D="
        src_port = "-sP="
        dst_port = "-dP="
        name = "-N="

        src_name = str(request.POST["nodes[0][name]"])
        dst_name = str(request.POST["nodes[1][name]"])
        for sw in json_device["Switches"]:
            if (str(sw["name"]) == src_name):
                src += str(sw["DatapathId"])
            elif (str(sw["name"]) == dst_name):
                dst += str(sw["DatapathId"])

        src_port_name = str(request.POST['nodes[0][physical]'])
        dst_port_name = str(request.POST['nodes[1][physical]'])
        src_port += src_port_name.split("/")[2]
        dst_port += dst_port_name.split("/")[2]

        post_name = str(request.POST['name'])
        for ch in [" ", "/"]:
            if ch in post_name:
                post_name.replace(ch, '_')
        name += post_name

        try:
            json.loads(check_output([p, path, cmd, src,
                                    dst, src_port,
                                    dst_port, name]).decode('utf-8'))
            name += "_backward"
            new_src = "-S=" + dst[3:]
            new_dst = "-D=" + src[3:]
            new_src_port = "-sP=" + dst_port[4:]
            new_dst_port = "-dP=" + src_port[4:]
            json.loads(check_output([p, path, cmd, new_src,
                                    new_dst, new_src_port,
                                    new_dst_port, name]).decode('utf-8'))
        except CalledProcessError:
            return HttpResponse('fail')

        response = dict()
        response["text"] = "success"
        response["name"] = post_name
        return JsonResponse(response)
    else:
        return render(request, 'devices/index_service_add.html',
                      {'node': topology_generator()})


def service_detail_view(request, pk):
    ##
    json_device = get_of_local()
    # json_device = get_of_prod()
    if (json_device["Switches"] == "no data"):
        data_flag = False
    else:
        data_flag = True
    ##
    services = get_services_local()
    # services = get_services_prod()
    if (services["tunnels"] == "no data"):
        raise Http404("No such service!")
    else:
        for serv in services["tunnels"]:
            if (str(serv["name"]).replace("/", "_") == pk):
                path_arr = serv["path"]["nodes"]
                path = ""
                for node in path_arr:
                    added = False
                    for sw in json_device["Switches"]:
                        if (str(node) == sw["DatapathId"]):
                            path += str(sw["name"])
                            added = True
                    if (added is False):
                        legacy = Device.objects.get(cust_ip=str(Int2IP(node)))
                        path += legacy.hostname
                    path += ","
                path = path[0:-1]

                tunnels_array = list()
                temp_dict = dict()
                temp_dict["name"] = str(serv["name"]).replace("/", "_")
                temp_dict["src_port"] = "Ethernet1/0/" + str(serv["src_port"])
                temp_dict["dst_port"] = "Ethernet1/0/" + str(serv["dst_port"])
                temp_dict["active_path"] = serv["active_path"]
                if (data_flag is True):
                    for sw in json_device["Switches"]:
                        if (str(serv["src"]) == sw["DatapathId"]):
                            temp_dict["src"] = sw["name"]
                        elif (str(serv["dst"]) == sw["DatapathId"]):
                            temp_dict["dst"] = sw["name"]
                else:
                    temp_dict["src"] = serv["src"]
                    temp_dict["dst"] = serv["dst"]
                tunnels_array.append(temp_dict)

                return render(request, 'devices/index_service_detail.html',
                              {'node': topology_generator(),
                               'service': tunnels_array,
                               'path': path})
        raise Http404("No such service!")


@csrf_exempt
def service_list_view(request):
    if request.method == 'POST':
        post_name = str(request.POST['name'])

        p = "python"
        path = "/root/projects/marrow/modules-uspace/marrow.py"
        cmd = "remove-tunnel"
        name = "-N=" + post_name

        name.replace("_backward", "")

        response = dict()
        response["name"] = post_name
        try:
            json.loads(check_output([p, path, cmd, name]).decode('utf-8'))
            name += "_backward"
            json.loads(check_output([p, path, cmd, name]).decode('utf-8'))
            response["text"] = "success"
        except CalledProcessError:
            return HttpResponse('fail')
            response["text"] = "fail"

        return JsonResponse(response)
    else:
        ##
        json_device = get_of_local()
        # json_device = get_of_prod()
        if (json_device["Switches"] == "no data"):
            data_flag = False
        else:
            data_flag = True
        ##
        services = get_services_local()
        # services = get_services_prod()
        if (services["tunnels"] == "no data"):
            return render(request, 'devices/index_services_list.html')
        else:
            tunnels_array = list()
            for serv in services["tunnels"]:
                temp_dict = dict()
                temp_dict["name"] = str(serv["name"]).replace("/", "_")
                temp_dict["src_port"] = "Ethernet1/0/" + str(serv["src_port"])
                temp_dict["dst_port"] = "Ethernet1/0/" + str(serv["dst_port"])
                if (data_flag is True):
                    for sw in json_device["Switches"]:
                        if (str(serv["src"]) == sw["DatapathId"]):
                            temp_dict["src"] = sw["name"]
                        elif (str(serv["dst"]) == sw["DatapathId"]):
                            temp_dict["dst"] = sw["name"]
                else:
                    temp_dict["src"] = serv["src"]
                    temp_dict["dst"] = serv["dst"]
                tunnels_array.append(temp_dict)

            return render(request, 'devices/index_services_list.html',
                          {'services': tunnels_array})


@csrf_exempt
def topo_refresh(request):
    ##
    links_data = get_topo_local()
    # links_data = get_topo_prod()
    if (links_data["nodes"] == 0):
        json_data = dict()
        json_data["text"] = "fail"
        return JsonResponse(json_data)
    ##
    ofsw_data = get_of_local()
    # ofsw_data = get_of_prod()
    if (ofsw_data["Switches"] == "no data"):
        json_data = dict()
        json_data["text"] = "fail"
        return JsonResponse(json_data)

    ofsw_data.pop('Links')
    temp_arr = list()
    for node in links_data["nodes"]:
        for link in node['l']:
            if ((link["t"] == "U") and (link["ST"] == 0)):
                add = True
                for element in temp_arr:
                    if (element["source"] == link["N"] and
                       element["target"] == node["id"]):
                            add = False
                if add:
                    temp_dict = dict()
                    temp_dict["source"] = node["id"]
                    temp_dict["target"] = link["N"]
                    temp_arr.append(temp_dict)
        node.pop('l')
    links_data.update({'links': temp_arr})
    links_data.pop('nodes')
    links_data["text"] = "success"

    temp123 = list()
    for node in ofsw_data["Switches"]:
        if (node["state"] == "0"):
            temp123.append(node["name"])

    return JsonResponse({"links_data": links_data, "ofsw_data": temp123})


@csrf_exempt
def service_refresh(request):
    ##
    services_data = get_services_local()
    # services_data = get_services_prod()
    if (services_data["tunnels"] == "no data"):
        json_data = dict()
        json_data["text"] = "fail"
        return JsonResponse(json_data)
    ##
    ofsw_data = get_of_local()
    # ofsw_data = get_of_prod()
    if (ofsw_data["Switches"] == "no data"):
        json_data = dict()
        json_data["text"] = "fail"
        return JsonResponse(json_data)

    req_type = str(request.POST["type"])
    pk = str(request.POST["name"])

    for serv in services_data["tunnels"]:
        if (str(serv["name"]).replace("/", "_") == pk):
            if (req_type == "part"):
                active_path = serv["active_path"]
                return JsonResponse({"active_path": active_path})
            path_arr = serv["path"]["nodes"]
            path = ""
            for node in path_arr:
                added = False
                for sw in ofsw_data["Switches"]:
                    if (str(node) == sw["DatapathId"]):
                        path += str(sw["name"])
                        added = True
                if (added is False):
                    legacy = Device.objects.get(cust_ip=str(Int2IP(node)))
                    path += legacy.hostname
                path += ","
            path = path[0:-1]

        return JsonResponse({"path": path})
