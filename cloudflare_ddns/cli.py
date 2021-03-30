#!/usr/bin/python
import argparse
from sys import exit
from cloudflare_ddns.utils import write_data, load_data
import requests
from cloudflare_ddns.__init__ import CloudFlareConnection
from appdirs import user_config_dir


def gen_settings(path):
    """genrate ~/.config/cloudflareddns/settings.yml"""
    api_key = input("enter your api key: ")  # nosec
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    print("verifying api key")
    response = requests.get(
        "https://api.cloudflare.com/client/v4/user/tokens/verify", headers=headers
    )
    if response.status_code != 200:
        print("error verifying key exiting")
        exit(1)
    else:
        if response.json()["success"] != True:
            print("error verifying key exiting")
            exit(1)
    print("verified api key")
    zone = input("Please enter your zone id: ")  # nosec
    num_domains = int(input("number of domains including the root domain: "))  # nosec
    domains = []
    if num_domains < 0:
        print("you need at least 1 domain")
        exit(1)
    for i in range(0, num_domains):
        domain = ""
        while len(domain) == 0:
            domain = input(f"input the domain for the {i+1} domain: ")  # nosec
        domains.append(domain)
    print("genrating record ids please wait.")
    records = []

    response = requests.get(
        f"https://api.cloudflare.com/client/v4/zones/{zone}/dns_records",
        headers=headers,
    )
    for domain in domains:
        failed = True
        for record in response.json()["result"]:
            if record["name"] == domain and record["type"] == "A":
                records.append(record["id"])
                failed = False
        if failed == True:
            print(f"{domain} did not have a record exiting")
            exit(1)

    data = {"zone": zone, "api_key": api_key, "domains": domains, "records": records}
    write_data(data, path)


def main():
    """pareser arguments"""
    parser = argparse.ArgumentParser(prog="cloudflare-ddns")
    parser.add_argument(
        "--gensettings",
        action="store_true",
        help="Genrate settings.yml, will be stored in",
    )
    parser.add_argument(
        "-f", nargs="?", const=None, type=str, help="force path for settings.yml"
    )
    args = parser.parse_args()
    if args.gensettings == True:
        if args.f == None:
            path = f"{user_config_dir(appname='cloudflareddns')}/settings.yml"
            gen_settings(path)
        else:
            gen_settings(args.f)
    else:
        if args.f == None:
            path = f"{user_config_dir(appname='cloudflareddns')}/settings.yml"
            settings = load_data(path)
        else:
            settings = load_data(path=args.f)
        connection = CloudFlareConnection(
            settings["api_key"],
            settings["zone"],
            settings["domains"],
            settings["records"],
        )
        connection.update_ips()


if __name__ == "__main__":
    main()