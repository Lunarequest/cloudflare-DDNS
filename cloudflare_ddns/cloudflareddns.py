#!/usr/bin/python3
import requests
import socket
import json
from requests.models import Response
import yaml
import logging
from sys import exit


def is_connected():
    """function to check if there is a internet connection returns true

    :return: bool (true if connected)
    """
    try:
        # creates connection if it is able too then it returns true
        x = socket.create_connection(("8.8.8.8", 53))
        x.close()
        return True
    except OSError as e:  # Generic os errors
        print(e)
    return False


def check_status(response):
    # checks if record exists
    if response.json()["errors"][0]["code"] == 81058:
        logging.error("there was a conficting domain please report this")
    else:
        # if there is a unknow error print some debug info
        print(
            "there was a error in the update the response may help debug it: \n",
            response,
            "\n",
            response.json(),
        )

def ip_update(domain, zone_id,record_id, headers):
    dynamic_ip = str(
        requests.get("http://api64.ipify.org?format=json").json()["ip"]).strip()
            # prepares data for json injection to update via api
    data = {
                "type": "A",
                "name": f"{domain}",
                "content": f"{dynamic_ip}",
                "ttl": 1,
                "proxied": True,
            }
            # dumps as json
    data = json.dumps(data)
    response = requests.put(
                f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}",
                headers=headers,
                data=data,
            )
    # checks if resposne returns a 200
    if response.status_code == 200:
        print(f"updated {domain}")
    else:
        check_status(response)
        exit(1)

def make_request(headers, zone_id, record_id):
    response = requests.get(
        f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}",
        headers=headers,
    )
    return response

def update(domains, zone_id, record_ids, api_key):
    """updates the ip

    :param domains: (array) The domain
    :param zone_id: (str) The domains zone id can be found in the cloudflare dashbboard
    :param record_ids: (array) The record id
    :param api_key: (str) The api key used to make requests

    :return: bool true if update succeeded false if failed
    """
    # get dynamic ip and ensure it is a string with out any sepcial charecters. the change is too support ipv6
    dynamic_ip = str(
        requests.get("http://api64.ipify.org?format=json").json()["ip"]
    ).strip()
    # create request headers
    headers = {"content-type": "application/json", "Authorization": f"Bearer {api_key}"}
    # gets the record via api
    response=make_request(headers,zone_id,record_ids[1])
    # extracts the ip
    ip = str(response.json()["result"]["content"])
    # compares the current public ip with the one set in cloud flare
    if str(ip) == str(dynamic_ip):
        # if set prints warrning
        print(f"ips for domains/subdomains in this zone are already set")
        return False
    else:
        index = 0
        for domain in domains:
            logging.info("current ip: " + dynamic_ip, "cloudflare ip: " + ip)
            check = ip_update(domain,zone_id,record_ids[index], headers)
            index+=1
        return True
            


def ddns():
    """
    runs dynamic ddns after reading from the settings.yml file

    :return: None
    """
    # gets settings
    with open("settings.yml", "r") as f:
        settings = yaml.safe_load(f.read())
        domain = settings["domain"]
        api_key = settings["api_key"]
        zone_id = settings["zone_id"]
        record_id = settings["record_id"]
        # trys getting subdomains
        try:
            subdomains = settings["subdoamins"]
            subdomains_id = settings["subdomains_id"]
            f.close()
            domains = []
            domains.append("domain")
            for domain_name in subdomains:  # updates each subdomain
                domains.append(domain_name)
            record_ids = []
            record_ids.append(record_id)
            for record in subdomains_id:
                record_ids.append(record)
            update(domains,zone_id,record_ids,api_key)
        except:  # expects if subdomains do exist
            f.close()
            domains = []
            domains.append(domain)
            record_ids = []
            record_ids.append(record_id)
            update(domains, zone_id, record_ids, api_key)

def parse_data(data, domain):
    for record in data:
        if record["name"] == domain and record["type"] == "A":
            record_id = record["id"]
            return record_id
    return None

def verify_data(data):
    if len(data["subdoamins"]) == len(data["subdomains_id"]):
        return data
    else:
        print("unable to get record id of one or  more subdomain")
        exit(1)


def get_record(api_key, zone_id):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    response = requests.get(
        f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records",
        headers=headers,
    )
    return response


def get_record_id(settings):
    """
    gets record ids using settings which uses the dict returned from read data

    :returns: dict{api_key,domain,zone_id,record_id, subdomains, domains_id}
    api_key,domain,zone_id,record_id are of the type string
    subdomains, domains_id are lists
    """
    api_key = settings["api_key"]
    domain = settings["domain"]
    zone_id = settings["zone_id"]
    response = get_record(api_key, zone_id)
    data = response.json()  # loads the json response
    data = data["result"]
    record_id = parse_data(data, domain)
    if record_id == None:
        print("failed to get record id")
        exit(1)
    if settings["subdoamins"]:
        subdomain = settings["subdoamins"]
        domains_id = []
        for domains in subdomain:
            x = parse_data(data, domains)
            domains_id.append(x)
            # checks if all domains ids have subdomains
        data = {
            "api_key": api_key,
            "domain": domain,
            "zone_id": zone_id,
            "record_id": record_id,
            "subdoamins": subdomain,
            "subdomains_id": domains_id,
        }
        return data

    else:
        data = {
            "api_key": api_key,
            "domain": domain,
            "zone_id": zone_id,
            "record_id": record_id,
        }
        return data

if __name__ == "__main__":
    ddns()