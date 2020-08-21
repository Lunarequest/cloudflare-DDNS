#!/usr/bin/python
import yaml

email = input("input email: ")
api_key = input("input api_key: ")
domain = input("input target domain: ")

creds = {"email": email, "api_key": api_key, "domain": domain}
x = yaml.dump(creds)
with open("settings.yml", "w") as f:
    f.write(x)
    f.close()
