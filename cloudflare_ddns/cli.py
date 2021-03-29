#!/usr/bin/python
import argparse
from sys import exit
from cloudflare_ddns.utils import write_data, load_data
import requests
from .__init__ import CloudFlareConnection


def gen_settings():
    """genrate ~/.config/cloudflareddns/settings.yml"""
    api_key = input("enter your api key: ")
    zone = input("Please enter your zone id: ")
    num_domains = int(input("number of domains including the root domain: "))
    domains = []
    if num_domains < 0:
        print("you need at least 1 domain")
        exit(1)
    for i in range(0, num_domains):
        domain = ""
        while len(domain) == 0:
            domain = input(f"input the domain for the {i+1} domain: ")
        domains.append(domain)
    print("genrating record ids please wait.")
    records = []
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    response = requests.get(
        f"https://api.cloudflare.com/client/v4/zones/{zone}/dns_records",
        headers=headers,
    )
    for domain in domains:
        failed = True
        for record in response.json():
            if record["name"] == domain:
                records.append(record)
                failed = False
        if failed == True:
            print(f"{domain} did not have a record exiting")
            exit(1)

    data = {"zone": zone, "api_key": api_key, "domains": domains, "records": records}
    write_data(data)


def main():
    """pareser arguments"""
    parser = argparse.ArgumentParser(prog="cloudflare-ddns")
    parser.add_argument(
        "--gensettings",
        action="store_true",
        help="Genrate settings.yml, will be stored in",
    )
    args = parser.parse_args()
    if args.gensettings == True:
        gen_settings()
    else:
        settings = load_data()
        connection = CloudFlareConnection(
            settings["api_key"],
            settings["zone"],
            settings["domains"],
            settings["records"],
        )
        connection.update_ips()
