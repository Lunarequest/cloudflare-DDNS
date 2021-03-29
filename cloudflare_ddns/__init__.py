"""A python script to update dynamic ips"""
import requests
from typing import List
import logging
from .Exceptions import LenMissmatch

__version__ = "5.0.0"


class CloudFlareConnection:
    def __init__(
        self, api_key: str, zone: str, domains: List[str], record_ids: List[str]
    ):
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

    def update_ips(self):
        def make_request(headers, zone_id, record_id):
            response = requests.get(
                f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}",
                headers=headers,
            )
            return response

        current_ip = requests.get("http://api64.ipify.org?format=json").json()["ip"]
        for record in self.record_ids:
            response = make_request(self.headers, self.zone, record)
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

    def update_record(self, domain: str, ip: str, record: str) -> bool:
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
