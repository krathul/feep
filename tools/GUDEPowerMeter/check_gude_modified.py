#!/usr/bin/env python3

import requests
import json
import time
import subprocess

def main(ip, resolution, joules):
    url = f'http://{ip}/status.json'

    ONLY_VALUES = 0x4000
    cgi = {'components': ONLY_VALUES}  # simple-sensors + and only values

    resolution = float(resolution);

    target_sleep_time = resolution/1000.0

    while True: # loop until CTRL+C
        timestamp_before = time.time_ns()
        time.sleep(target_sleep_time)

        data = json.loads(requests.get(url, params=cgi, verify=False, auth=None).text)

        # print(data) # DEBUG
        timestamp_after = time.time_ns()
        effective_sleep_time = timestamp_after - timestamp_before
        # print(effective_sleep_time / 1_000_000_000) # DEBUG
        conversion_factor = effective_sleep_time / 1_000_000 # we want microjoule. Therefore / 10**9 to get seconds and then * 10**3 to get mJ
        if joules:
            print(int(timestamp_after / 1_000), int(data["sensor_values"][0]['values'][0][4]['v']*conversion_factor), flush=True)
        else:
            print(int(timestamp_after / 1_000), int(data["sensor_values"][0]['values'][0][4]['v']), flush=True)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", type=int, help="Resolution")
    parser.add_argument("-x", type=str, help="IP")
    parser.add_argument("--joules", action='store_true', help="Report Joules instead of Watts")

    args = parser.parse_args()

    if args.i is None:
        parser.print_help()
        print("Please supply -i to set resolution in milliseconds")
        exit(2)

    if args.x is None:
        parser.print_help()
        print("Please supply -x to set the IP where to find the JSON API from GUDE")
        exit(2)

    if args.joules is None:
        parser.print_help()
        print("Please supply --joules to switch to Joules reporting")
        exit(2)

    main(args.x, args.i, args.joules)
