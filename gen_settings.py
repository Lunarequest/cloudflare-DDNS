#!/usr/bin/python3
import yaml


def gen_settings():
    api_key = input("input api key: ")
    domain = input("input target domain: ")
    zone_id = input("input zone id: ")
    check = int(input("input number of subdomains: "))
    if check == 0:
        creds = {"api_key": api_key, "domain": domain, "zone_id": zone_id}
    else:
        subdomains = []
        for i in range(0, check):
            x = input("input subdomain: ")
            subdomains.append(x)
        creds = {
            "api_key": api_key,
            "domain": domain,
            "zone_id": zone_id,
            "subdoamins": subdomains,
        }
    x = yaml.dump(creds)
    with open(f"settings.yml", "w") as f:
        f.write(x)
        f.close()


if __name__ == "__main__":
    gen_settings()
