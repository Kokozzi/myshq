from django.db import models


class Device(models.Model):
    hostname = models.CharField(
        "Hostname", max_length=128, unique=True)
    ip = models.GenericIPAddressField(
        "IP Address", protocol='IPv4', unique=True)
    cust_ip = models.GenericIPAddressField(
        protocol='IPv4', blank=True, null=True)
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

    def __str__(self):
        return self.hostname
