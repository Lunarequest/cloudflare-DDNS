import yaml
from appdirs import user_config_dir


def write_data(data):
    """
    writes data to settings.yml
    :param data: (dict)
    :return: None
    """
    with open(f"{user_config_dir(appname='cloudflareddns')}/settings.yml", "w") as f:
        data = yaml.dump(data)
        f.write(data)
        f.close()


def load_data():
    """function to read data from settings.yml"""
    with open(f"{user_config_dir(appname='cloudflareddns')}/settings.yml", "r") as f:
        # opens settings.yml and loads
        settings = yaml.safe_load(f.read())
    f.close()
    return settings
