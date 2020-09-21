import requests

def make_requests(zone_id,record_id,api_key):
    """
    makes request for dns records for record id specifed

    :param zone_id: (str) zone id
    :param record_id: (str) dns record id
    :param api_key: (str) api key for cloudflare api

    :return response: (requests object) the response object
    """
    headers = {"content-type": "application/json", "Authorization": f"Bearer {api_key}"}
    response = requests.get(
            f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}",
            headers=headers,)
    return response

def request_status(response,requested):
    """
    function for internal use 
    """
    if response.status_code == 200:
        requested.append(response)
    else:
        global failed;failed=True
    return requested
def verify(settings):
    """
    function to verify all settings are valid.

    :param settings: (dict) needs to be in the form of the dict returned by read data
    :return: bool
    """
    global failed;failed = False
    requested = []
    zone_id = settings["zone_id"]
    api_key = settings["api_key"]
    record_id = settings["record_id"]
    response=make_requests(zone_id,record_id,api_key)
    requested=request_status(response,requested)
    if settings["subdoamins"] != None:
        for record_id in settings["subdomains_id"]:
            # gets the record via api
            response=make_requests(zone_id,record_id,api_key)
            requested=request_status(response,requested)
    return failed

    