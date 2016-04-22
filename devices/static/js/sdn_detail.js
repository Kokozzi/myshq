$(function () {

var msg = "Недоступны данные об устройстве",
    title = "Ошибка!",
    port_info = "";

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

if (data.nodes === 0) {
    toastr.error(msg, title);
    return;
}

$('#sdn_header_table tbody > tr').find('td:last').after('<td><h3>' + data.name + '</h3>' + data.TypeOfSwitch + '<br>' + data.IpAddress + '</td>');

$('#company').html(data.CompanyName);
$('#protocol_vers').html(data.ProtocolVersion);
$('#ip_conn').html(data.IpAddressConn);
$('#port').html(data.portNumber);
$('#hw_address').html(data.hardwareAddress);
$('#date_start_conn').html(data.DateStartConn);
$('#time_start_conn').html(data.TimeStartConn);
$('#serial').html(data.SN);
$('#config').html(data.config);
$('#curr_features').html(data.currentFeatures);
$('#advert_features').html(data.advertisedFeatures);
$('#supp_features').html(data.supportedFeatures);
$('#peer_features').html(data.peerFeatures);

for (var i = 0; i < data.Ports.length; i++) {
	if (data.Ports[i].connection_status === "up") {
		port_info += '<tr><th><h4><span class="label label-primary">' + data.Ports[i].name + '</span></h4></th>';
	} else {
		port_info += '<tr><th><h4><span class="label label-danger">' + data.Ports[i].name + '</span></h4></th>';
	}
	port_info += '<td>' + data.Ports[i].hw_addr + '</td><td>' + data.Ports[i]['TX bytes'] + '</td><td>' + data.Ports[i]['RX bytes'] + '</td><td>' + data.Ports[i]['Tx Pkts'] + '</td>';
	port_info += '<td>' + data.Ports[i]['RX Pkts'] + '</td><td>' + data.Ports[i]['Dropped'] + '</td><td>' + data.Ports[i]['Error'] + '</td></tr>';
}

$('#sdn_port_table tr:last').after(port_info);

});