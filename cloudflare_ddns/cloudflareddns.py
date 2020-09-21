#!/usr/bin/python3
import requests
import socket
import json
import yaml
import logging
from ipaddress import ip_address
from sys import exit, argv
from cloudflare_ddns.verify import verify

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


def update(domain, zone_id, record_id, api_key):
    """updates the ip

    :param domain: (str) The domain
    :param zone_id: (str) The domains zone id can be found in the cloudflare dashbboard
    :param record_id: (str) The record id
    :param api_key: (str) The api key used to make requests

    :return: bool true if update succeeded false if failed
    """
    # get dynamic ip and ensure it is a string with out any sepcial charecters. the change is too support ipv6
    dynamic_ip = str(requests.get("http://api64.ipify.org?format=json").json()["ip"]).strip()
    # create request headers
    headers = {"content-type": "application/json", "Authorization": f"Bearer {api_key}"}
    # gets the record via api
    response = requests.get(
        f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}",
        headers=headers,
    )
    # extracts the ip
    ip = str(response.json()["result"]["content"])
    # compares the current public ip with the one set in cloud flare
    if ip_address(ip) == ip_address(dynamic_ip):
        # if set prints warrning
        print(f"ip for {domain} is already set")
    else:
        logging.info("current ip: " + dynamic_ip, "cloudflare ip: " + ip)
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
        response_status = response.json()["success"]
        if response_status:
            print(f"updated {domain}")
            return True
        else:
            # checks if record exists
            if response.json()["errors"][0]["code"] == 81058:
                logging.error("there was a conficting domain please report this")
                return False
            else:
                # if there is a unknow error print some debug info
                print(
                    "there was a error in the update the response may help debug it: \n",
                    response,
                    "\n",
                    response.json(),
                )
                return False


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
            update(domain, zone_id, record_id, api_key)  # updates root domain
            index = 0
            for domain_name in subdomains:  # updates each subdomain
                domain_id = subdomains_id[index]
                index = +1
                update(domain_name, zone_id, domain_id, api_key)
        except:  # expects if subdomains do exist
            f.close()
            update(domain, zone_id, record_id, api_key)

def write_data(data):
    """writes data to settings.yml

    :param data: (dict)  the dict is the same as returned by get_record_id
    
    :return: None
    """
    with open("settings.yml", "w") as f:
        data = yaml.dump(data)
        f.write(data)
        f.close()
def read_data():
    """function to read data from settings.yml"""
    with open("settings.yml", "r") as f:
        # opens settings.yml and loads
        settings = yaml.safe_load(f.read())
        domain = settings["domain"]
        api_key = settings["api_key"]
        zone_id = settings["zone_id"]
        try:
            subdomain = settings["subdoamins"]
        except:
            subdomain = None
        f.close()
    data = {
                        "api_key": api_key,
                        "domain": domain,
                        "zone_id": zone_id,
                        "subdoamins": subdomain}
    return data
def read_data_record():
    """function to read data include record ids from settings.yml"""
    with open("settings.yml", "r") as f:
        # opens settings.yml and loads
        settings = yaml.safe_load(f.read())
        domain = settings["domain"]
        api_key = settings["api_key"]
        zone_id = settings["zone_id"]
        record_id = settings["record_id"]
        try:
            subdomain = settings["subdoamins"]
            subdomains_id = settings["subdomains_id"]
        except:
            subdomain = None
            subdomains_id = None
        f.close()
    data = {
                            "api_key": api_key,
                            "domain": domain,
                            "zone_id": zone_id,
                            "record_id":record_id,
                            "subdoamins": subdomain,
                            "subdomains_id":subdomains_id
                            }
    return data
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
        # creates headers for request
    headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
    response = requests.get(
            f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records",
            headers=headers,
        )
    data = response.json()  # loads the json response
    data = data["result"]
    record_id = None
        # parese the data until all records have data
    for record in data:
            if record["name"] == domain and record["type"] == "A":
                record_id = record["id"]
    if record_id != None:
        if settings["subdoamins"] !=None:
                subdomain = settings["subdoamins"]
                domains_id = []
                for record in data:
                    for domains in subdomain:
                        if str(record["name"]) == str(domains):
                            x = record["id"]
                            domains_id.append(x)
                # checks if all domains ids have subdomains
                if len(domains_id) != len(subdomain):
                    print("unable to get record id of one or  more subdomain")
                    exit(1)
                # updates settings
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
            