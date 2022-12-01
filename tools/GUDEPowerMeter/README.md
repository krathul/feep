Slimmed down version of check_gude.py from https://github.com/gudesystems/check_gude.py
for the Blauer Engel für Software Measurements
===============

- Create **venv**: `python3 -m venv venv`
- Activate: `source venv/bin/activate`
- Install requests: `pip3 install requests`
- Supply the `-i` parameter for the resolution in ms and the `-x` parameter for the IP
    + Example: `python3 check_gude_modified.py -i 100 -x 192.168.178.1`
   
The script reports the Watts by default. If you want Joules, which will be the integration
over the time since the last poll, supply `--joules`

