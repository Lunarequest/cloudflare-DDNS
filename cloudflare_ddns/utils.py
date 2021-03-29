import yaml
from appdirs import user_config_dir
import os
from typing import Dict


def write_data(data: Dict[str, str]):
    """
    writes data to settings.yml
    Args:
        data (dict): dict to convert to yaml to write to settings.yml

    Returns:
        None
    """
    path = user_config_dir(appname="cloudflareddns")
    if os.path.exists(path) == False:
        os.mkdir(path)
    with open(f"{path}/settings.yml", "w") as f:
        yaml_to_write = yaml.dump(data)
        f.write(yaml_to_write)
        f.close()


def load_data():
    """function to read data from settings.yml"""
    with open(f"{user_config_dir(appname='cloudflareddns')}/settings.yml", "r") as f:
        # opens settings.yml and loads
        settings = yaml.safe_load(f.read())
    f.close()
    return settings
