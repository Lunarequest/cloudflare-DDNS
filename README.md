# CloudFlare DDNS

<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
[![Maintainability](https://api.codeclimate.com/v1/badges/aaca3fe4da8a8389f639/maintainability)](https://codeclimate.com/github/advaithm/cloudflare-DDNS/maintainability)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

This script will update cloudflare dns with new dynamic ips when the current one changes. Please check the settings.yml file to ensure its correct.

## Limitations

- No Offcial IPv6 support(My isp does not assing ipv6 address I can not test if this works)

If you wish to conrtbute to this project please check the [CONTRIBUTING.md](https://github.com/advaithm/cloudflare-DDNS/blob/master/CONTRIBUTING.md) file.

The scipt can be got at <https://pypi.org/project/simple-cloudflare-ddns/>.

```bash
$ cloudflareddns --gen-settings # this will create a file called settings.yml at ~/config/cloudflareddns/
$ cloudflareddns # this will update all ips
```
**VERSION 5.0 is incompatible with any pervious versions due to a rewrite of how data is handled**