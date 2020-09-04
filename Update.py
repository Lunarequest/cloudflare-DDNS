#!/usr/bin/python
from aifc import Error
from unittest import result
import requests
import socket
import json
import yaml
import argparse
from sys import exit


def is_connected():
    try:
        x = socket.create_connection(("8.8.8.8", 53))
        x.close()
        return True
    except Error as e:
        print(e)
    return False


def update(domain, zone_id, record_id, api_key):
    dynamic_ip = requests.get("http://ip.42.pl/raw").text
    headers = {"content-type": "application/json", "Authorization": f"Bearer {api_key}"}

    response = requests.get(
        f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}",
        headers=headers,
    )
    ip = response.json()["result"]["content"]
    if ip == dynamic_ip:
        print(f"ip for {domain} is already set")
    else:
        data = {
            "type": "A",
            "name": f"{domain}",
            "content": f"{dynamic_ip}",
            "ttl": 1,
            "proxied": True,
        }
        data = json.dumps(data)
        response = requests.put(
            f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}",
            headers=headers,
            data=data,
        )
        response_status = response.json()["success"]
        if response_status:
            print(f"updated {domain}")
        else:
            print(
                "there was a error in the update the response may help debug it\n",
                response,
                "\n",
                response.json(),
            )


def ddns():
    with open("settings.yml", "r") as f:
        settings = yaml.safe_load(f.read())
        domain = settings["domain"]
        api_key = settings["api_key"]
        zone_id = settings["zone_id"]
        record_id = settings["record_id"]
        try:
            subdomains = settings["subdoamins"]
            subdomains_id = settings["subdomains_id"]
            f.close()
            update(domain, zone_id, record_id, api_key)
            index = 0
            for domain_name in subdomains:
                domain_id = subdomains_id[index]
                index = +1
                print(domain_name)
                update(domain_name, zone_id, domain_id, api_key)
        except Error:
            f.close()
            update(domain, zone_id, record_id, api_key)


def get_record_id():
    with open("settings.yml", "r") as f:
        settings = yaml.safe_load(f.read())
        domain = settings["domain"]
        api_key = settings["api_key"]
        zone_id = settings["zone_id"]
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        response = requests.get(
            f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records",
            headers=headers,
        )
        data = response.json()
        data = data["result"]
        for record in data:
            if record["name"] == domain and record["type"] == "A":
                record_id = record["id"]
        try:

            subdomain = settings["subdoamins"]
            f.close()
            domains_id = []
            for record in data:
                for domain in subdomain:
                    if str(record["name"]) == str(domain):
                        x = record["id"]
                        domains_id.append(x)
            with open("settings.yml", "w") as f:
                data = {
                    "api_key": api_key,
                    "domain": domain,
                    "zone_id": zone_id,
                    "record_id": record_id,
                    "subdoamins": subdomain,
                    "subdomains_id": domains_id,
                }
                data = yaml.dump(data)
                f.write(data)
                f.close()
        except Error:
            with open("settings.yml", "w") as f:
                data = {
                    "api_key": api_key,
                    "domain": domain,
                    "zone_id": zone_id,
                    "record_id": record_id,
                }
                data = yaml.dump(data)
                f.write(data)
                f.close()


parser = argparse.ArgumentParser()
parser.add_argument("--ddns", type=bool, help="update dns records")
x = parser.parse_args()
if x.ddns:
    connected = False
    while connected == False:
        connected = is_connected()
    ddns()
else:
    connected = False
    while connected == False:
        connected = is_connected()
    get_record_id()
    ddns()