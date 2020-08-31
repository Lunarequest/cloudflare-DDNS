#!/usr/bin/pyth
from requests import get
import yaml
import CloudFlare
import sys
import os


def get_zone_ip(zone, domain):
    found = False
    print(zones)
    for zone in zones:
        zone_name = zone["name"]
        if zone_name == domain:
            found = True
            zone_id = zone["id"]
    if found:
        return zone_id
    else:
        print("zone not found")
        sys.exit(1)


def get_record_id(zone_id):
    record_id = cf.zones.dns_records(zone_id)
    return record_id


def check(zone_id, record_id):
    dns_records = cf.zones.dns_records.get(zone_id)
    current_ip = get("http://ip.42.pl/raw").text
    if current_ip == dns_records["conntent"]:
        print("ip is up to date")
    else:
        dns_records = cf.zones.dns_records.edit(zone_id, record_id, current_ip)


def update():
    path = os.path.expanduser("~/.local")
    try:
        with open(f"{path}/settings.yml", "r") as f:
            data = f.read()
            creds = yaml.full_load(data)
            f.close()
        email = creds["email"]
        api_key = creds["api_key"]
        domain = creds["domain"]
        zones = creds["zones"]
        global cf
        cf = CloudFlare.CloudFlare(email=email, token=api_key)
    except:
        print("failed to open config")
        sys.exit(1)
    message = """
        THIS PROGRAM DOES NOT COME WITH ANY WARRENTY
        """
        print(message)
    for zone in zones:
        zonex = cf.zones.get()
        if len(zonex) < 1:
            print("no zone in account")
        zone_id = get_zone_ip(zonex, domain)
        record_id = get_record_id(zone_id)
        check(record_id, zone_id)


if __name__ == "__main__":
    pass
