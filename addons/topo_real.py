import json

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
                temp_dict["bw_up"] = link["BW"]
                temp_arr.append(temp_dict)
    node.pop('l')

print(temp_arr)

json_data.update({'links': temp_arr})
# print(json_data)
