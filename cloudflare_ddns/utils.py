import yaml
import os
from typing import Dict, Optional


def write_data(data, path):
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


def load_data(path):
    """
    function to read data from path
    Args:
        path (str):(optional) path to load data from.
    """
    with open(path, "r") as f:
        # opens settings.yml and loads
        settings = yaml.safe_load(f.read())
    f.close()
    return settings
