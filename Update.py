#!/usr/bin/python3
import requests
import socket
import json
import yaml
from ipaddress import ip_address
from sys import exit, argv

# function to check if there is a internet connection
def is_connected():
    try:
        # creates connection if it is able too then it returns true
        x = socket.create_connection(("8.8.8.8", 53))
        x.close()
        return True
    except OSError as e:  # Generic os errors
        print(e)
    return False


# updates the ip
def update(domain, zone_id, record_id, api_key):
    # get dynamic ip and ensure it is a string with out any sepcial charecters
    dynamic_ip = str(requests.get("http://ipinfo.io/ip").text.strip())
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
        exit
    else:
        print("current ip: " + dynamic_ip, "cloudflare ip: " + ip)
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
        else:
            # checks if record exists
            if response.json()["errors"][0]["code"] == 81058:
                print("there was a conficting domain please report this")
            else:
                # if there is a unknow error print some debug info
                print(
                    "there was a error in the update the response may help debug it: \n",
                    response,
                    "\n",
                    response.json(),
                )


def ddns():
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


# udates settings.yml with record ids
def get_record_id():
    # Trys with multiple domains
    with open("settings.yml", "r") as f:
        # opens settings.yml and loads
        settings = yaml.safe_load(f.read())
        domain = settings["domain"]
        api_key = settings["api_key"]
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
            try:
                subdomain = settings["subdoamins"]
                f.close()
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
            except:
                # excepts running with root domain
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
        else:
            print("unable to find record id")
            exit(1)


# check if argv has a argument
if len(argv) < 2:
    connected = False
    while connected == False:
        connected = is_connected()
    get_record_id()
    ddns()
# check if that argument is --ddns
elif argv[1] == "--ddns":
    # check if internet is connected
    connected = False
    while connected == False:
        connected = is_connected()
    ddns()
# check for usage info
elif argv[1] == "-h":
    print(
        "usage update.py <args:optional>\n-h for this message\n--ddns skip directly to DDNS updateing"
    )
else:
    # error out
    print("Too many args. ")
