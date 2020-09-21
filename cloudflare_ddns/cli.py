from cloudflare_ddns.cloudflareddns import is_connected, read_data_record, verify, read_data, get_record_id, write_data, ddns
from cloudflare_ddns.gen_settings import gen_settings
from sys import argv
def main():
    # check if argv has a argument
    if len(argv)== 1:
        connected = False
        while connected is False:
            connected = is_connected()
        settings = read_data()
        data = get_record_id(settings)
        write_data(data)
        ddns()
    # check if that argument is --ddns
    if len(argv) == 2:
        if argv[1] == "--ddns":
            # check if internet is connected
            connected = False
            while connected == False:
                connected = is_connected()
            ddns()
        elif argv[1] == "--gen-settings":
            gen_settings()
        elif argv[1] == "--verify":
            settings = read_data_record()
            failed = verify(settings)
            if failed == True:
                print("settings has failed the intgerty check")
            else:
                print("settings has passed the intgerty check")
    # check for usage info handel
    elif argv[1] == "-h":
        print(
            "usage update.py <args:optional>\n-h for this message\n--gen-settings to create settings.yml\n--ddns skip directly to DDNS updateing"
        )
    else:
        # error out
        print("Too many args. ")
if __name__ == "__main__":
    main()