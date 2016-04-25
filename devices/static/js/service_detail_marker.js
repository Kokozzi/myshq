$(document).ready(function(){

	var path_array = String(path).split(','),
			names = d3.selectAll("text")[0],
	        links = d3.selectAll("path")[0];

    document.getElementById("service_name").innerHTML = "Сервис: " + String(service.name);

	 for (var i = 0; i < names.length; i += 1) {
	 	if ((names[i].innerHTML == path_array[0]) || (names[i].innerHTML == path_array[path_array.length - 1])) {
	 		names[i].innerHTML += "(Узел доступа)";
            names[i].style.fontSize = 14;
            names[i].style.fontWeight = "bold";
            names[i].style.fontStyle = "italic";
	 	}
	 }

    for (var i = 0; i < (path_array.length - 1); i += 1) {
        for (var j = 0; j < data.links.length; j += 1) {
            if ((links[j].__data__.name === (path_array[i] + "-" + path_array[i+1])) || (links[j].__data__.name === (path_array[i+1] + "-" + path_array[i]))) {
                links[j].attributes[0].value = "service_link";
                links[j].attributes.service = 1;
            }
        }
    }

    var timerId = setInterval(function() {
        $.get(URL, function (response) {
            if (response.links_data.text === 'success') {
                for (var i = 0; i < response.links_data.links.length; i += 1) {
                    if (response.links_data.links[i].status === 0) {
                        for (var j = 0; j < data.links.length; j += 1) {
                            if ((links[j].__data__.source.DatapathId == response.links_data.links[i].source) && (links[j].__data__.target.DatapathId == response.links_data.links[i].target)) {
                                links[j].attributes[0].value = "down_link";
                            }
                        }
                    }
                }
                $(" image ").each(function () {
                    for (var i = 0; i < response.ofsw_data.length; i += 1) {
                        if ($(this)[0].__data__.name == response.ofsw_data[i]) {
                            $(this)[0].attributes[0].value = "../../../static/img/switch-d.svg";
                        }
                    } 
                });
                // console.log(response);
                /*$(" path ").each(function () {
                console.log($(this))
                if ($(this)[0].__data__.status === 0){
                    $(this)[0].attributes[0].value = "down_link";
                } else {
                    if ($(this)[0].attributes.service === 1) {
                        $(this)[0].attributes[0].value = "service_link";
                    } else {
                        $(this)[0].attributes[0].value = "link";
                    }
                }      
                });*/
            } else {
            }
        }); 

      
        
    }, 2000);

});