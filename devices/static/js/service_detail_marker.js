$(document).ready(function(){

	var path_array = String(path).split(','),
			names = d3.selectAll("text")[0],
	        links = d3.selectAll("path")[0],
            curr_active_path = service[0].active_path

    document.getElementById("service_name").innerHTML = "Сервис: " + String(service[0].name);

    service_mark(path_array);

    var request = {};
    request["name"] = service[0].name;
    
    var path_refresh = setInterval(function() {
        request["type"] = "part";
        $.post(URL_service, request, function (response) {
            if (response.active_path != curr_active_path) {
                request["type"] = "full";
                $.post(URL_service, request, function(resp) {
                    curr_path = String(resp.path).split(',');

                    for (var j = 0; j < data.links.length; j += 1) {
                        links[j].attributes[0].value = "link";
                        links[j].attributes.service = 0;
                    }   

                    console.log(curr_path);

                    for (var i = 0; i < (curr_path.length - 1); i += 1) {
                        for (var j = 0; j < data.links.length; j += 1) {
                            if ((links[j].__data__.name === (curr_path[i] + "-" + curr_path[i+1])) || (links[j].__data__.name === (curr_path[i+1] + "-" + curr_path[i]))) {
                                links[j].attributes[0].value = "service_link";
                                links[j].attributes.service = 1;
                            }
                        }
                    }
                    curr_active_path = response.active_path;
                });
            }
        });
    }, 2000);


    function service_mark(arr) {
        for (var i = 0; i < names.length; i += 1) {
            if ((names[i].innerHTML == arr[0]) || (names[i].innerHTML == arr[arr.length - 1])) {
                names[i].innerHTML += "(Узел доступа)";
                names[i].style.fontSize = 14;
                names[i].style.fontWeight = "bold";
                names[i].style.fontStyle = "italic";
            }
        }

        for (var i = 0; i < (arr.length - 1); i += 1) {
            for (var j = 0; j < data.links.length; j += 1) {
                if ((links[j].__data__.name === (arr[i] + "-" + arr[i+1])) || (links[j].__data__.name === (arr[i+1] + "-" + arr[i]))) {
                    links[j].attributes[0].value = "service_link";
                    links[j].attributes.service = 1;
                }
            }
        }
    }
});