#!/usr/bin/python
import argparse
from Update import update
import gen_settings
import Update
import os

if os.getuid() != 0:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--init", type=bool, default=False, help="toggle genrate settings"
    )
    args = parser.parse_args()
    if args.init:
        gen_settings.gen_settings()
        Update.update()
    else:
        Update.update
else:
    print("Do not run this script as root")
