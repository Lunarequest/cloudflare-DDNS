from requests import get
import yaml
import CloudFlare
import sys

with open("settings.yml", "r") as f:
    data = f.read()
    creds = yaml.full_load(data)
    f.close()
    email = creds["email"]
    api_key = creds["api_key"]
    domain = creds["domain"]
    global cf
    cf = CloudFlare.CloudFlare(email=email, token=api_key)

zone = None
ip = None
dns = []
zones = cf.zones.get()
if len(zones) < 1:
    print("no zone in account")
    sys.exit(1)


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


def check(zone_id):
    dns_records = cf.zones.dns_records.get(zone_id)
    current_ip = get("http://ip.42.pl/raw").text
    if current_ip == dns_records["conntent"]:
        print("ip is up to date")
    else:
        dns_records = cf.zones.dns_records.edit(zone_id, current_ip)


message = """
THIS PROGRAM DOES NOT COME WITH ANY WARRENTY
"""
print(message)
zone_id = get_zone_ip(zones, domain)
check(cf, zone_id)

