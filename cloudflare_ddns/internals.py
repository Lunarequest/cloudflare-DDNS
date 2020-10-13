import yaml

"""all functions here can not be used by other programs"""


def check_returned(check_update):
    if check_update:
        force = True
    else:
        force = False
    return force


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
        "subdoamins": subdomain,
    }
    return data


def read_data_record():
    """function to read data include record ids from settings.yml """
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
        "record_id": record_id,
        "subdoamins": subdomain,
        "subdomains_id": subdomains_id,
    }
    return data