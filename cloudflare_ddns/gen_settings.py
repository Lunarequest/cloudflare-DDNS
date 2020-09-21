import yaml,logging
def gen_settings():
    """function to genrate the settings.yaml
    :return: None
    """
    api_key = input("input api key: ").strip().replace(" ","")
    domain = input("input target domain: ").strip().replace(" ","")
    zone_id = input("input zone id: ").strip().replace(" ","")
    check = int(input("input number of subdomains: "))
    if check == 0:
        creds = {"api_key": api_key, "domain": domain, "zone_id": zone_id}
    else:
        subdomains = []
        for i in range(0, check):
            x = input("input subdomain: ").strip().replace(" ","")
            subdomains.append(x)
        creds = {
            "api_key": api_key,
            "domain": domain,
            "zone_id": zone_id,
            "subdoamins": subdomains,
        }
    x = yaml.dump(creds)
    logging.info(creds)
    with open(f"settings.yml", "w") as f:
        f.write(x)
        f.close()
