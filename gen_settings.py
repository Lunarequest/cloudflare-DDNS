import yaml
import os


def gen_settings():
    email = input("input email: ")
    api_key = input("input api_key: ")
    domain = input("input target domain: ")
    record_id = input("input record id: ")

    creds = {"email": email, "api_key": api_key, "domain": domain, "id": record_id}
    x = yaml.dump(creds)
    path = os.path.expanduser("~/.local")
    with open(f"{path}/settings.yml", "w") as f:
        f.write(x)
        f.close()


if __name__ == "__main__":
    pass
