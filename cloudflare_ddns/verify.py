import requests

def verify(settings):
    """
    function to verify all settings are valid.

    :param settings: (dict) needs to be in the form of the dict returned by read data
    """
    failed = False
    requested = []
    zone_id = settings["zone_id"]
    api_key = settings["api_key"]
    record_id = settings["record_id"]
    headers = {"content-type": "application/json", "Authorization": f"Bearer {api_key}"}
    response = requests.get(
            f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}",
            headers=headers,)
    if response.status_code == 200:
        requested.append(response)
    else:
        failed=True
        return failed
    if settings["subdoamins"] != None:
        for record_id in settings["subdomains_id"]:
            # gets the record via api
            response = requests.get(
            f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}",
            headers=headers,)       
            if response.status_code==200:
                for old_request in requested:
                    if response.json()==old_request.json():
                            failed= True
            else:
                failed = True
    return failed

    