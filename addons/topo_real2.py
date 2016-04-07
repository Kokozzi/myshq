import json

with open("/home/tsibulya/sdn/devices/topo_real.json") as json_file:
    json_data = json.load(json_file)

temp_arr = list()

for node in json_data["nodes"]:
    node["name"] = node["id"]
    node["status"] = 1
    for link in node['l']:
        temp_dict = dict()
        add = True
        for element in temp_arr:
            if (element["source"] == node["id"] and
               element["target"] == link["N"]):
                    if link["t"] == "U":
                        element["bw_up"] = link["BW"]
                    if link["t"] == "D":
                        element["bw_dn"] = link["BW"]
                    add = False

            if add:
                temp_dict["source"] = node["id"]
                temp_dict["target"] = link["N"]
                temp_dict["port_src"] = link["P1"]
                temp_dict["port_dst"] = link["P2"]
                temp_dict["status"] = link["ST"]
                if link["t"] == "U":
                    temp_dict["bw_up"] = link["BW"]
                if link["t"] == "D":
                    temp_dict["bw_dn"] = link["BW"]
                temp_arr.append(temp_dict)
    node.pop('l')

print(temp_arr)

json_data.update({'links': temp_arr})
# print(json_data)
