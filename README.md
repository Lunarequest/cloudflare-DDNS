# CloudFlare DDNS

<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
[![Coverage Status](https://coveralls.io/repos/github/advaithm/cloudflare-DDNS/badge.svg?branch=master)](https://coveralls.io/github/advaithm/cloudflare-DDNS?branch=master)

This script will update cloudflare dns with new dynamic ips when the current one changes. Please check the settings.yml file to ensure its correct.

## Limitations

- No IPv6 support(My isp does not assing ipv6 address I can not test if this works)

If you wish to conrtbute to this project please check the [CONTRIBUTING.md](https://github.com/advaithm/cloudflare-DDNS/blob/master/CONTRIBUTING.md) file.

The scipt can be got at <https://pypi.org/project/simple-cloudflare-ddns/>. I will be publishing docs on how to use the inbuilt functions. For a quick setup you can use the following commands.

```bash
$ cloudflareddns --gen-settings # this will create a file called settings.yml
$ cloudflareddns # this will get record ids
```

after running this you can run `cloudflareddns --ddns` to skip getting the record id as it is stored in the settings.yml
You can verify if the settings.yml is correct by running `cloudflareddns --verify`
