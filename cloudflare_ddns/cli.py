#!/usr/bin/python
from cloudflare_ddns.cloudflareddns import (
    is_connected,
    get_record_id,
    ddns,
    verify_data,
)
from cloudflare_ddns.gen_settings import gen_settings, edit, edit_api, add_subdomain
from cloudflare_ddns.verify import verify
from cloudflare_ddns.internals import read_data_record, read_data, write_data
from sys import argv, exit


def getrecords():
    settings = read_data()
    data = get_record_id(settings)
    data = verify_data(data)
    write_data(data)
    ddns()


def verify_record():
    settings = read_data_record()
    failed = verify(settings)
    if failed == True:
        print("settings has failed the intgerty check")
        exit(0)
    print("settings has passed the intgerty check")
    # check for usage info handel


def check_connection():
    connected = False
    while connected is False:
        connected = is_connected()


def edit_chose(arg):
    if arg == "--edit":
        edit()
    elif arg == "--edit-api":
        edit_api()
    else:
        print(
            "usage update.py <args:optional>\n-h for this message\n--gen-settings to create settings.yml\n--ddns skip directly to DDNS updateing"
        )


def subdomain(arg):
    if arg == "--add-subdomain":
        add_subdomain()
    else:
        print(
            "usage update.py <args:optional>\n-h for this message\n--gen-settings to create settings.yml\n--ddns skip directly to DDNS updateing"
        )


def check_arugment(argument):
    if argument == "--gen-settings":
        gen_settings()
    elif argument == "--verify":
        verify_record()
    elif argument.contains("subdomain"):
        subdomain(argument)
    elif argument.contains("--edit"):
        edit_chose(argument)
    else:
        print(
            "usage update.py <args:optional>\n-h for this message\n--gen-settings to create settings.yml\n--ddns skip directly to DDNS updateing"
        )


def argv_handle(agrv):
    argument = argv[1]
    if argument == "--ddns":
        ddns()
    else:
        check_arugment(argument)


def check_args(num_experssions):
    if num_experssions == 1:
        getrecords()
    elif num_experssions == 2:
        argv_handle(argv)
    else:
        # error out
        print("Too many args. ")


def main():
    check_connection()
    num_experssions = len(argv)
    check_args(num_experssions)


if __name__ == "__main__":
    main()
