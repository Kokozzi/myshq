$(document).ready(function(){

	var links = d3.selectAll("path")[0],
        current_links = [],
        current_nodes = [];

    var timerId = setInterval(function() {
        $.get(URL, function (response) {
            if (response.links_data.text === 'success') {

                /*LINKS*/

                if (response.links_data.links.length !== 0 && current_links.length === 0) {
                    for (var i = 0; i < response.links_data.links.length; i += 1) {
                        for (var j = 0; j < data.links.length; j += 1) {
                            if ((links[j].__data__.source.DatapathId == response.links_data.links[i].source) && (links[j].__data__.target.DatapathId == response.links_data.links[i].target)) {
                                links[j].attributes[0].value = "down_link";
                            }
                            if ((links[j].__data__.target.DatapathId == response.links_data.links[i].source) && (links[j].__data__.source.DatapathId == response.links_data.links[i].target)) {
                                links[j].attributes[0].value = "down_link";
                            }
                        }
                    }
                    current_links = response.links_data.links; 
                }

                if (response.links_data.links.length === 0 && current_links.length !== 0) {
                    for (var j = 0; j < data.links.length; j += 1) {
                        if (links[j].attributes[0].value == "down_link") {
                            links[j].attributes[0].value = "link";
                        }
                    }
                    current_links = response.links_data.links;
                }

                if (response.links_data.links.length !== 0 && current_links.length !== 0) {
                    
                    var diff_links = $(response.links_data.links).not(current_links).get();

                    if (diff_links.length !== 0) {
                        for (var j = 0; j < data.links.length; j += 1) {
                            if (links[j].attributes[0].value == "down_link") {
                                links[j].attributes[0].value = "link";
                            }
                        }
                        for (var i = 0; i < response.links_data.links.length; i += 1) {
                            for (var j = 0; j < data.links.length; j += 1) {
                                if ((links[j].__data__.source.DatapathId == response.links_data.links[i].source) && (links[j].__data__.target.DatapathId == response.links_data.links[i].target)) {
                                    links[j].attributes[0].value = "down_link";
                                }
                                if ((links[j].__data__.target.DatapathId == response.links_data.links[i].source) && (links[j].__data__.source.DatapathId == response.links_data.links[i].target)) {
                                    links[j].attributes[0].value = "down_link";
                                }
                            }
                        }
                    current_links = response.links_data.links;
                    }
                }

                /*NODES*/

                if (response.ofsw_data.length !== 0 && current_nodes.length === 0) {
                    $(" image ").each(function () {
                        for (var i = 0; i < response.ofsw_data.length; i += 1) {
                            if ($(this)[0].__data__.name == response.ofsw_data[i]) {
                                if ($(this)[0].attributes[0].value == "../../../static/img/switch.svg") {
                                    $(this)[0].attributes[0].value = "../../../static/img/switch-d.svg";
                                }
                                if ($(this)[0].attributes[0].value == "../../../static/img/router.svg") {
                                    $(this)[0].attributes[0].value = "../../../static/img/router-d.svg";
                                }
                            }
                        } 
                    });
                    current_nodes = response.ofsw_data; 
                }

                if (response.ofsw_data.length === 0 && current_nodes.length !== 0) {
                    $(" image ").each(function () {
                        if ($(this)[0].attributes[0].value == "../../../static/img/switch-d.svg") {
                            $(this)[0].attributes[0].value = "../../../static/img/switch.svg";
                        }
                        if ($(this)[0].attributes[0].value == "../../../static/img/router-d.svg") {
                            $(this)[0].attributes[0].value = "../../../static/img/router.svg";
                        } 
                    });
                    current_nodes = response.ofsw_data; 
                }

                if (response.ofsw_data.length !== 0 && current_nodes.length !== 0) {

                    var diff_nodes = $(current_nodes).not(response.ofsw_data).get(),
                        diff_nodes2 = $(response.ofsw_data).not(current_nodes).get();

                    if (Math.max(diff_nodes.length, diff_nodes2.length) !== 0) {
                        $(" image ").each(function () {
                            if ($(this)[0].attributes[0].value == "../../../static/img/switch-d.svg") {
                                $(this)[0].attributes[0].value = "../../../static/img/switch.svg";
                            }
                            if ($(this)[0].attributes[0].value == "../../../static/img/router-d.svg") {
                                $(this)[0].attributes[0].value = "../../../static/img/router.svg";
                            }
                            for (var i = 0; i < response.ofsw_data.length; i += 1) {
                                if ($(this)[0].__data__.name == response.ofsw_data[i]) {
                                    if ($(this)[0].attributes[0].value == "../../../static/img/switch.svg") {
                                        $(this)[0].attributes[0].value = "../../../static/img/switch-d.svg";
                                    }
                                    if ($(this)[0].attributes[0].value == "../../../static/img/router.svg") {
                                        $(this)[0].attributes[0].value = "../../../static/img/router-d.svg";
                                    }
                                }
                            } 
                        });
                        current_nodes = response.ofsw_data; 
                    }
                }
            }
        }); 

    }, 1000);

});