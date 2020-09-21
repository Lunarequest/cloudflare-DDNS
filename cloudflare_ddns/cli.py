from cloudflare_ddns.cloudflareddns import is_connected, read_data_record, verify, read_data, get_record_id, write_data, ddns
from cloudflare_ddns.gen_settings import gen_settings
from sys import argv, exit

def getrecords():
    settings = read_data()
    data = get_record_id(settings)
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
       

def main():
    connected = False
    while connected is False:
        connected = is_connected()
    num_experssions = len(argv)
    if num_experssions == 1:
        getrecords()
    elif num_experssions == 2:
        argument = argv[1]
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
    else:
        # error out
        print("Too many args. ")
if __name__ == "__main__":
    main()