import yaml
import os


def gen_settings():
    api_key = input("input api key: ")
    domain = input("input target domain: ")
    zone_id = input("input zone id:")

    creds = {"api_key": api_key, "domain": domain, "zone_id": zone_id}
    x = yaml.dump(creds)
    with open(f"settings.yml", "w") as f:
        f.write(x)
        f.close()


if __name__ == "__main__":
    gen_settings()
