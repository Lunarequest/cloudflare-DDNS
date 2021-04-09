#!/usr/bin/python
import argparse
from sys import exit
from .utils import write_data, load_data, veirfy_api_key, genrate_record_ids
from .cloudflare import CloudFlareConnection
from .Exceptions import LenMissmatch
from appdirs import user_config_dir


def gen_settings(path):
    """
    genrate settings.yml
    Args:
        path(str): path to settings.yml
    """
    api_key = input("enter your api key: ")  # nosec
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    print("verifying api key")
    valid_key = veirfy_api_key(api_key)
    if valid_key == False:
        print("the provied key was not valid")
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
    records = genrate_record_ids(domains, headers, zone)
    if len(records) != len(domains):
        raise LenMissmatch
    data = {"zone": zone, "api_key": api_key, "domains": domains, "records": records}
    write_data(data, path)


def remove_domain(path: str):
    """
    remove domain from settings.yml
    Args:
        path (str): path to settings.yml
    """
    settings = load_data(path)
    if len(settings["domains"]) == 1:
        print("you need at least one domain")
        exit(1)
    count = 1
    for i in settings["domains"]:
        print(f"{count}. {i}")
    domain_to_remove = int(
        input("input the number next to the domain you want to remove: ")  # nosec
    )
    settings["domains"].pop(domain_to_remove)
    headers = {
        "Authorization": f"Bearer {settings['api_key']}",
        "Content-Type": "application/json",
    }
    records = genrate_record_ids(settings["domains"], headers, settings["zone"])
    settings["records"] = records
    write_data(settings, path)


def add_domain(path):
    """
    function to add domain, 
    Args:
        path (str): path to settings.yml
    """
    settings = load_data(path)
    new_domain = input("input the domain: ")# nosec
    settings["domains"].append(new_domain)
    headers = {
        "Authorization": f"Bearer {settings['api_key']}",
        "Content-Type": "application/json",
    }
    settings["records"] = genrate_record_ids(settings["domains"],headers,settings["zone"])
    write_data(settings,path)

def update_api_key(path: str):
    settings = load_data(path)
    settings["api_key"] = input("please input the new api key: ")  # nosec
    print("verifying api key")  # nosec
    valid_key = veirfy_api_key(settings["api_key"])
    if valid_key == False:
        print("the provied key was not valid")
        exit(1)
    print("verified api key")
    write_data(settings, path)
    print("updated api key")

def update_domain(path:str):
    settings = load_data(path)
    if len(settings["domains"]) == 1:
        print("you need at least one domain")
        exit(1)
    count = 1
    for i in settings["domains"]:
        print(f"{count}. {i}")
    domain_to_remove = int(
        input("input the number next to the domain you want to remove: ")  # nosec
    )
    settings["domains"][domain_to_remove] = input(f"enter new value for domain {settings['domains'][domain_to_remove]}: ") # nosec
    write_data(settings,path)

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
    parser.add_argument("--updateapikey", action="store_true", help="update api key")
    parser.add_argument(
        "--removedomain", action="store_true", help="remove a domain from settings.yml"
    )
    parser.add_argument("--updatedomain",action="store_true", help="updated a domain from settings.yml")
    parser.add_argument("--adddomain",action="store_true", help="add a domain too settings.yml")
    args = parser.parse_args()
    if args.f == None:
        path = f"{user_config_dir(appname='cloudflareddns')}/settings.yml"
        settings = load_data(path)
    else:
        path = args.f

    if args.updateapikey == True:
        update_api_key(path)
    elif args.removedomain == True:
        remove_domain(path)
    elif args.adddomain == True:
        add_domain(path)
    elif args.updatedomain == True:
        update_domain(path)
    elif args.gensettings == True:
        gen_settings(path)
    else:
        settings = load_data(path)
        connection = CloudFlareConnection(
            settings["api_key"],
            settings["zone"],
            settings["domains"],
            settings["records"],
        )
        updated = connection.update_ips()
        if updated:
            print("updated domains to new ip")


if __name__ == "__main__":
    main()
