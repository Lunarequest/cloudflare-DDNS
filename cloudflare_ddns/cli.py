#!/usr/bin/python
from cloudflare_ddns.cloudflareddns import is_connected, get_record_id, ddns, verify_data
from cloudflare_ddns.gen_settings import gen_settings, edit, edit_api
from cloudflare_ddns.verify import verify
from cloudflare_ddns.internals import  read_data_record, read_data, write_data
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
def check_arugment(argument):
    if argument == "--ddns":
        ddns()
    elif  argument == "--gen-settings":
        gen_settings()
    elif argument == "--verify":
        verify_record()
    elif argument == "-h":
        print(
                "usage update.py <args:optional>\n-h for this message\n--gen-settings to create settings.yml\n--ddns skip directly to DDNS updateing"
            )
    elif argument=="--edit":
        edit()
    elif argument=="--edit-api":
        edit_api()
def main():
    check_connection
    num_experssions = len(argv)
    if num_experssions == 1:
        getrecords()
    elif num_experssions == 2:
        argument = argv[1]
        check_arugment(argument)
    else:
        # error out
        print("Too many args. ")
if __name__ == "__main__":
    main()
