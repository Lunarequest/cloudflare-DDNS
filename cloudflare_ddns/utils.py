import yaml
import os
from typing import Dict, List, Optional
import requests


def write_data(data: Dict[str, str], path: str):
    """
    writes data to path
    Args:
        data (dict): dict to convert to yaml to write to settings.yml
        path (str): Optional
    Returns:
        None
    """
    if path.endswith("/"):
        if os.path.exists(path) == False:
            os.mkdir(path)
    with open(path, "w") as f:
        yaml_to_write = yaml.dump(data)
        f.write(yaml_to_write)
        f.close()


def load_data(path: str) -> Dict[str, str]:
    """
    function to read data from path
    Args:
        path (str):(optional) path to load data from.
    Returns:
        settings (Dict): setttings read from the file
    """
    with open(path, "r") as f:
        # opens settings.yml and loads
        settings = yaml.safe_load(f.read())
    f.close()
    return settings


def veirfy_api_key(api_key: str) -> bool:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    response = requests.get(
        "https://api.cloudflare.com/client/v4/user/tokens/verify", headers=headers
    )
    if response.status_code != 200:
        print("error verifying key exiting")
        return False
    else:
        if response.json()["success"] != True:
            print("error verifying key exiting")
            return False
    return True


def genrate_record_ids(
    domains: List[str], headers: dict[str, str], zone_id: str
) -> List[str]:
    records = []
    response = requests.get(
        f"https://api.cloudflare.com/client/v4/zones/{zone}/dns_records",
        headers=headers,
    ).json()["result"]
    for domain in domains:
        record = in_array(domain,response)
        if record:
            records.append(record)
    return records


def in_array(domain: str, response) -> Optional[str]:
        for record in response:
            if record["name"] == domain and record["type"] == "A":
                return record
    return None