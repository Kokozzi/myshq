from django.db import models


class Device(models.Model):
    hostname = models.CharField(
        "Hostname", max_length=128, unique=True)
    ip = models.GenericIPAddressField(
        "IP Address", protocol='IPv4', unique=True)
    community = models.CharField(
        "SNMP Community", max_length=40, blank=True, default='public')

    sysname = models.CharField(max_length=128, blank=True, null=True)
    hardware = models.CharField(max_length=50, blank=True, null=True)
    os = models.CharField(max_length=50, blank=True, null=True)
    serial = models.CharField(max_length=30, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    uptime = models.IntegerField(blank=True, null=True)

    status = models.IntegerField(default=0)
    last_polled = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    icon = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return self.hostname


class SDN_Device(models.Model):
    hostname = models.CharField(
        "Hostname", max_length=128, unique=True)
    ip = models.GenericIPAddressField(
        "IP Address", protocol='IPv4', blank=True, null=True)
    ip_conn = models.GenericIPAddressField(
        protocol='IPv4', blank=True, null=True)
    port = models.IntegerField(blank=True, null=True)
    hw_address = models.CharField(max_length=20, blank=True)
    date_start_conn = models.DateField(blank=True, null=True)
    time_start_conn = models.TimeField(blank=True, null=True)
    company = models.CharField(max_length=128, blank=True)
    device_type = models.CharField(max_length=60, blank=True)
    protocol_vers = models.FloatField(blank=True, null=True)
    serial = models.CharField(max_length=30, blank=True)
    config = models.CharField(max_length=100, blank=True)
    status = models.IntegerField(default=0)
    curr_features = models.CharField(max_length=150, blank=True)
    advert_features = models.CharField(max_length=150, blank=True)
    supp_features = models.CharField(max_length=150, blank=True)
    peer_features = models.CharField(max_length=150, blank=True)
    last_polled = models.DateTimeField()

    def __str__(self):
        return self.hostname


class SDN_Port(models.Model):
    hostname = models.ForeignKey('SDN_Device', on_delete=models.CASCADE,)
    name = models.CharField("Interface Name", max_length=128)
    hw_address = models.CharField(max_length=20, blank=True)
    status = models.IntegerField(default=0)
    tx_bytes = models.IntegerField(blank=True, null=True)
    rx_bytes = models.IntegerField(blank=True, null=True)
    tx_packets = models.IntegerField(blank=True, null=True)
    rx_packets = models.IntegerField(blank=True, null=True)
    dropped = models.IntegerField(blank=True, null=True)
    errored = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name
