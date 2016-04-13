$(document).ready(function(){
    $("#form").steps({
        bodyTag: "fieldset",

        labels: {
            finish: "Завершить",
            next: "Далее",
            previous: "Назад",
            loading: "Загрузка ..."
        },

        onStepChanging: function (event, currentIndex, newIndex)
        {
            // Always allow going backward even if the current step contains invalid fields!
            if (currentIndex > newIndex)
            {
                return true;
            }

            var form = $(this);

            // Clean up if user went backward before
            if (currentIndex < newIndex)
            {
                // To remove error styles
                $(".body:eq(" + newIndex + ") label.error", form).remove();
                $(".body:eq(" + newIndex + ") .error", form).removeClass("error");
            }

            var dev_count = document.getElementById("device_count").innerHTML;

            if (currentIndex > 0) {
               if (dev_count === "Всего добавлено узлов: 0" || dev_count === "Всего добавлено узлов: 1") {
                toastr.error("Добавьте хотя бы два узла!", "Ошибка!");
                return false;
                } 
            }

            // Disable validation on fields that are disabled or hidden.
            form.validate().settings.ignore = ":disabled,:hidden";

            // Start validation; Prevent going forward if false
            return form.valid();
        },
        onStepChanged: function (event, currentIndex, priorIndex)
        {
            var table = $("#all_dev_table tbody")[0],
                names = d3.selectAll("text")[0],
                links = d3.selectAll("path")[0],
                html = "";
            
            if (currentIndex === 1) {
                $("#name_header")[0].innerHTML = "Добавление сервиса: " + $("#serviceName").val();
                
                for (var i = 0; i < names.length; i += 1) {
                    names[i].innerHTML = names[i].innerHTML.replace(" (Узел доступа)","");
                    names[i].style.fontSize = 12;
                    names[i].style.fontWeight = "normal";
                }
                d3.selectAll("path")
                    .attr("class", "link");
            }
            
            if (currentIndex === 2 && priorIndex === 1)
            {
                $(".select2_demo_2").select2();
                
                var divStyle = $('.back-change')[0].style;                
                
                d3.selectAll("text")
                    .style("font-size", 12)
                    .style("font-weight", "normal");
                d3.selectAll("path")
                    .attr("class", "link");

                for (var i = 0; i < names.length; i+= 1) {
                    for (var j = 1; j < table.rows.length; j += 1) {
                        if (table.rows[j].cells[1].innerHTML === names[i].innerHTML) {
                            names[i].innerHTML += " (Узел доступа)";
                            names[i].style.fontSize = 14;
                            names[i].style.fontWeight = "bold";
                            names[i].style.fontStyle = "italic";
                        }
                    }
                }
                
                for (var i = 0; i < names.length; i += 1) {
                    if (names[i].innerHTML.search("(Обязательно)") !== -1) {
                        names[i].style.fontSize = 12;
                        names[i].style.fontWeight = "bold";
                        names[i].style.fontStyle = "italic";
                    }   
                }
                
                $("#link_list :selected").each(function () {
                for (var i = 0; i < links.length; i += 1) {
                    if ($(this).val() === links[i].__data__.name) {
                        links[i].attributes[0].value = "active_link";
                    }
                }
                });
                  
            }
        },
        onFinishing: function (event, currentIndex)
        {
            var form = $(this);
            form.validate().settings.ignore = ":disabled";
            return form.valid();
        },
        onFinished: function (event, currentIndex)
        {
            var table = $("#all_dev_table tbody")[0],
                i = 1;

            result["name"] = $("#serviceName").val();
            result["nodes"] = [];
            for (i = 1; i < table.rows.length; i += 1) {
                var node = {};
                node["name"] = table.rows[i].cells[1].innerHTML;
                if (table.rows[i].cells[2].innerHTML === '<i class="fa fa-times text-danger"></i>') {
                    node["physical"] = "";
                } else {
                    node["physical"] = table.rows[i].cells[2].innerHTML;
                }
                if (table.rows[i].cells[3].innerHTML === '<i class="fa fa-times text-danger"></i>') {
                    node["ip"] = "";
                } else {
                    node["ip"] = table.rows[i].cells[3].innerHTML;
                }
                if (table.rows[i].cells[4].innerHTML === '<i class="fa fa-times text-danger"></i>') {
                    node["port"] = "";
                } else {
                    node["port"] = table.rows[i].cells[4].innerHTML;
                }
                result["nodes"].push(node);
            }
            result["bw"] = $("#bw_input").val();
            result["req_nodes"] = [];
            result["req_links"] = [];
            
            $("#node_list :selected").each(function () {
                result["req_nodes"].push($(this).val());
            });
            
            $("#link_list :selected").each(function () {
                result["req_links"].push($(this).val());
            });
            
            console.log(result);
        }
    }).validate({
                errorPlacement: function (error, element)
                {
                    element.before(error);
                },
                rules: {
                    confirm: {
                        equalTo: "#password"
                    }
                }
            });
});