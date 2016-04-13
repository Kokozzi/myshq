$(function () {
    function input_check(input) {
        if (input === "") {
            return '<i class="fa fa-times text-danger"></i>';
        } else {
            return input;
        }
    }
    
    function validate_ip(raw_ip) {
        var ipformat = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
        if (raw_ip.match(ipformat)) {
            return true;
        } else {
            return false;
        }
    }
    
    function validate_port(raw_port) {
        if (raw_port === '<i class="fa fa-times text-danger"></i>') {
            return raw_port;
        } else {
            if ($("#inlineRadio1").is(":checked") === true) {
                raw_port += " TCP";
            } else {
                raw_port += " UDP";
            }
            return raw_port;
        }
    }
    
    var add_button = document.getElementById("device_add"),
        del_button = document.getElementById("dev_delete"),
        node_add = document.getElementById("node_add"),
        table = $("#all_dev_table tbody")[0],
        
        handler_add = function () {
            var msg = "",
                title = "Ошибка!",
                dev = document.getElementById("select_device").title,
                port = input_check(document.getElementById("port_select").value),
                ip = input_check(document.getElementById("ip_input").value),
                udp_port = input_check(document.getElementById("udp_port_input").value),
                flag = true,
                i = 1,
                j = 1,
                leng = 0,
                names = d3.selectAll("text")[0],
                links = d3.selectAll("path")[0],
                html = "";
            
            toastr.options = {
                "closeButton": false,
                "debug": false,
                "progressBar": true,
                "preventDuplicates": false,
                "positionClass": "toast-top-right",
                "onclick": null,
                "showDuration": "400",
                "hideDuration": "1000",
                "timeOut": "7000",
                "extendedTimeOut": "1000",
                "showEasing": "swing",
                "hideEasing": "linear",
                "showMethod": "fadeIn",
                "hideMethod": "fadeOut"
            };
            
            if (dev === "") {
                msg = "Выберите один из узлов!";
                toastr.error(msg, title);
                return;
            }

            if (port === ip && port === udp_port) {
                msg = "Выберите хотя бы один из параметров!";
                toastr.error(msg, title);
                return;
            }
            
            if (ip !== '<i class="fa fa-times text-danger"></i>' && validate_ip(ip) === false) {
                msg = "Введен некорректный IP-Адрес!";
                toastr.error(msg, title);
                return;
            }
            
            udp_port = validate_port(udp_port);

            for (i = 1; i < table.rows.length; i += 1) {
                if (table.rows[i].cells[1].innerHTML === dev) {
                    flag = false;
                    table.rows[i].cells[2].innerHTML = port;
                    table.rows[i].cells[3].innerHTML = ip;
                    table.rows[i].cells[4].innerHTML = udp_port;
                }
            }

            if (flag === true) {
                $('#all_dev_table tr:last').after('<tr><td><input type="checkbox" class="i-checks" name="input[]"></td><td>' + dev + '</td><td>' + port + '</td><td>' + ip + '</td><td>' + udp_port + '</td></tr>');
            }
            
            for (i = 0; i < names.length; i += 1) {
                flag = true;
                for (j = 1; j < table.rows.length; j += 1) {
                    if (table.rows[j].cells[1].innerHTML === names[i].innerHTML) {
                        flag = false;
                    }
                }
                if (flag === true) {
                    html += '<option value="' + names[i].innerHTML + '">' + names[i].innerHTML +'</option>';
                }
            }
            
            $("#node_list").html(html);

            html = "";

            for (var i = 0; i < links.length; i += 1) {
                html += '<option value="' + links[i].__data__.name + '">' + links[i].__data__.name +'</option>'; 
            }
            $("#link_list").html(html);
            
            leng = table.rows.length - 1;
            document.getElementById("device_count").innerHTML = "Всего добавлено узлов: " + leng;
        },

        handler_delete = function () {
            var del_array = [],
                pointer = 0,
                i = 1,
                leng = 0;

            for (i = 1; i < table.rows.length; i += 1) {
                var row = $("#all_dev_table tbody tr")[i],
                    nnn = $(row).find("input").eq(0);
                if ($(nnn).is(":checked") === true) {
                    del_array[pointer] = i;
                    pointer += 1;
                }
            }

            for (i = del_array.length - 1; i >= 0; i -= 1) {
                $("#all_dev_table tbody tr")[del_array[i]].remove();
            }
            
            leng = table.rows.length - 1;
            document.getElementById("device_count").innerHTML = "Всего добавлено узлов: " + leng;
        },
    
        handler_require = function () {
            var names = d3.selectAll("text")[0],
                links = d3.selectAll("path")[0];
            
            for (var i = 0; i < names.length; i += 1) {
                if (names[i].innerHTML.search("(Обязательно)") !== -1) {
                    names[i].innerHTML = names[i].innerHTML.replace(" (Обязательно)","");
                    names[i].style.fontSize = 12;
                    names[i].style.fontWeight = "normal";
                    names[i].style.fontStyle = "normal";
                }
            }
            
            $("#node_list :selected").each(function () {
                for (var i = 0; i < names.length; i += 1) {
                    if ($(this).val() === names[i].innerHTML) {
                        names[i].innerHTML += " (Обязательно)";
                        names[i].style.fontSize = 12;
                        names[i].style.fontWeight = "bold";
                        names[i].style.fontStyle = "italic";
                    }
                }
            });
            
            d3.selectAll("path")
                .attr("class", "link");
            
            $("#link_list :selected").each(function () {
                for (var i = 0; i < links.length; i += 1) {
                    if ($(this).val() === links[i].__data__.name) {
                        links[i].attributes[0].value = "active_link";
                    }
                }
            });
        };

    add_button.addEventListener("click", handler_add, false);
    del_button.addEventListener("click", handler_delete, false);
    node_add.addEventListener("click", handler_require, false);
});