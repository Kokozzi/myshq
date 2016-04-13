$(function () {
    
    // used to store the number of links between two nodes. 
    // mLinkNum[data.links[i].source + "," + data.links[i].target] = data.links[i].linkindex;
    var mLinkNum = {};

    // sort links first
    sortLinks();

    // set up linkIndex and linkNumer, because it may possible multiple links share the same source and target node
    setLinkIndexAndNum();

    var w = document.getElementById('page-wrapper').offsetWidth*0.95,
        h = document.documentElement.clientHeight*0.4;

    var force = d3.layout.force()
                  .size([w, h])
                  .linkDistance(250)
                  .charge(-3000)
                  .on("tick", tick);

    var drag = force.drag()
                    .on("dragstart", dragstart);

        force
            .nodes(d3.values(data.nodes))
            .links(data.links)
            .start();

    var svg = d3.select(".graphContainer").append("svg:svg")
                .attr("width", w)
                .attr("height", h);

    var path = svg.append("svg:g")
                  .selectAll("path")
                  .data(force.links())
                  .enter().append("svg:path")
                  .attr("class", "link")
                  .on("click", onClickLink);
        path.append("svg:title")
                    .text(function(d, i) { return d.name; });
    
    var circle = svg.selectAll(".circle")
                    .data(force.nodes())
                    .enter().append("g")
                    .attr("class", "circle")
                    .on("click", OnClickNode)
                    .call(force.drag);
        circle.append("svg:image")
                    .attr("xlink:href", function(d) { return d.icon; })
                    .attr("x", "-25px")
                    .attr("y", "-25px")
                    .attr("cursor", "pointer")
                    .attr("width", "75px")
                    .attr("height", "75px");
        circle.append("svg:text")
                    .attr("x", 50)
                    .attr("y", ".51em")
                    .style("font-size", 12)
                    .style("font-family", "sans-serif")
                    .text(function(d) { return d.name; });

    function OnClickNode(d) {
        var currentNode = d3.select(this).select("text")[0][0].innerHTML,
            names = d3.selectAll("text")[0],
            arr = [];
        
        arr = currentNode.split(' ');
        if (arr[arr.length - 1] === 'доступа)' || arr[arr.length - 1] === '(Обязательно)') {
            return;
        }
        
        for (var i = 0; i < names.length; i += 1) {
            arr = names[i].innerHTML.split(' ');
            if (arr[arr.length - 1] !== 'доступа)' && arr[arr.length - 1] !== '(Обязательно)') {
                if (names[i].innerHTML === currentNode) {
                    names[i].style.fontSize = 16;
                    names[i].style.fontWeight = "bold";
                } else {
                    names[i].style.fontSize = 12;
                    names[i].style.fontWeight = "normal";
                }
                d3.selectAll("path")
                    .attr("class", "link");
            }
        }
        
        document.getElementById("select_device").innerHTML = "Выбран узел: " + d.name;
        document.getElementById("select_device").title = d.name;
        document.getElementById("ip_input").value = "";
        document.getElementById("udp_port_input").value = "";
        var html = "<option></option>";
        for (var i = 0; i < d.Ports.length; i++) 
        {
            html += "<option>" + d.Ports[i].name + "</option>";
        }
        $("#port_select").html(html);
    } 

    function onClickLink(d) {
        d3.selectAll("text")
            .style("font-size", 12)
            .style("font-weight", "normal");
        d3.selectAll("path")
            .attr("class", "link");
        d3.select(this)
            .attr("class", "active_link");
    }


    // Use elliptical arc path segments to doubly-encode directionality.
    function tick() {

        circle.attr("x", function(d) { return d.x = Math.max(20, Math.min(w - 100, d.x)); })
              .attr("y", function(d) { return d.y = Math.max(20, Math.min(h - 50, d.y)); });

        path.attr("d", function(d) {
            // get the total link numbers between source and target node
            var lTotalLinkNum = mLinkNum[d.source.id + "," + d.target.id] || mLinkNum[d.target.id + "," + d.source.id];
            if(lTotalLinkNum > 1)
            {
                var dx = d.target.x - d.source.x,
                    dy = d.target.y - d.source.y,
                    dr = Math.sqrt(dx * dx + dy * dy);
                    // if there are multiple links between these two nodes, we need generate different dr for each path
                dr = dr/(1 + (1/lTotalLinkNum) * (d.linkindex - 1));
                    // generate svg path
                return "M" + d.source.x + "," + d.source.y + 
                        "A" + dr + "," + dr + " 0 0 1," + d.target.x + "," + d.target.y + 
                        "A" + dr + "," + dr + " 0 0 0," + d.source.x + "," + d.source.y; 
            }       
            // generate svg path
            return "M" + d.source.x + "," + d.source.y + "L" + d.target.x + "," + d.target.y;   
        });

        // Add tooltip to the connection path
        /*path.append("svg:title")
            .text(function(d, i) { return d.name; });*/

        circle.attr("transform", function(d) {
            return "translate(" + d.x + "," + d.y + ")";
        });
    } 

    function dragstart(d) {
      d3.select(this).classed("fixed", d.fixed = true);
    }


    // sort the links by source, then target
    function sortLinks()
    {                               
        data.links.sort(function(a,b) {
            if (a.source > b.source) 
            {
                return 1;
            }
            else if (a.source < b.source) 
            {
                return -1;
            }
            else 
            {
                if (a.target > b.target) 
                {
                    return 1;
                }
                if (a.target < b.target) 
                {
                    return -1;
                }
                else 
                {
                    return 0;
                }
            }
        });
    }

    //any links with duplicate source and target get an incremented 'linknum'
    function setLinkIndexAndNum()
    {                               
        for (var i = 0; i < data.links.length; i++) 
        {
            if (i != 0 &&
                data.links[i].source == data.links[i-1].source &&
                data.links[i].target == data.links[i-1].target) 
            {
                data.links[i].linkindex = data.links[i-1].linkindex + 1;
            }
            else 
            {
                data.links[i].linkindex = 1;
            }
            // save the total number of links between two nodes
            if(mLinkNum[data.links[i].target + "," + data.links[i].source] !== undefined)
            {
                mLinkNum[data.links[i].target + "," + data.links[i].source] = data.links[i].linkindex;
            }
            else
            {
                mLinkNum[data.links[i].source + "," + data.links[i].target] = data.links[i].linkindex;
            }
        }
    }   
});                          