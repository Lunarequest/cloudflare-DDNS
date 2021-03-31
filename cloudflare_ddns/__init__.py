"""A python script to update dynamic ips"""
import requests
from typing import List
import logging
from .Exceptions import LenMissmatch

__version__ = "5.0.0"


class CloudFlareConnection:
    """
    base class for working with the api
    """

    def __init__(
        self, api_key: str, zone: str, domains: List[str], record_ids: List[str]
    ):
        """
        Args:
            initalize data
            api_key (str): api key for cloudflare api
            zone (str): zone id in which domains exist
            domains (list): list of domains
        """
        if len(domains) == len(record_ids):
            self.api_key = api_key
            self.zone = zone
            self.domains = domains
            self.record_ids = record_ids
            self.headers = {
                "content-type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            }  # cloudlfare api auth
        else:
            raise LenMissmatch

    def make_request(self, record_id):
        response = requests.get(
            f"https://api.cloudflare.com/client/v4/zones/{self.zone}/dns_records/{record_id}",
            headers=self.headers,
        )
        return response

    def update_ips(self) -> bool:
        current_ip = requests.get("http://api64.ipify.org?format=json").json()["ip"]
        domains_updated = False
        for record in self.record_ids:
            response = self.make_request(record)
            ip = response.json()["result"]["content"]
            if ip != current_ip:
                if (
                    self.update_record(
                        self.domains[self.record_ids.index(record)], ip, record
                    )
                    == False
                ):
                    logging.error(
                        f"could not set ip for {self.domains[self.record_ids.index(record)]}"
                    )
                else:
                    logging.info(
                        f"updated ip for {self.domains[self.record_ids.index(record)]}"
                    )
                    domains_updated = True
        return domains_updated

    def update_record(self, domain: str, ip: str, record: str) -> bool:
        """
        updates the ip of a given record
        Args:
            domain (str): domain to update
            ip (str): ip to update too
            record (str): record id to update

        Returns:
            status (bool): True is ip is updated, False if it wasn't
        """
        data = {
            "type": "A",
            "name": f"{domain}",
            "content": f"{ip}",
            "ttl": 1,
            "proxied": True,
        }
        response = requests.put(
            f"https://api.cloudflare.com/client/v4/zones/{self.zone}/dns_records/{record}",
            headers=self.headers,
            data=data,
        )
        if response.status_code != 200:
            return False
        return True
