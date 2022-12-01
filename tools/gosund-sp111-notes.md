Gosund SP111 Setup
==================

(0) Prerequisite
----------------

- already flashed with a sufficiently new Tasmota version

(1) Firmware Reset
------------------

- if the device had previously been connected to another Wifi it might need a full reset before being able to connect to a new one
- if the device did open a WiFi access point named "tasmota-XXXXX" this is not needed, continue at (2) directly
- press the button for 40 seconds
- the device will restart and you should be able to continue at (2)

(2) WiFi Setup
--------------

- the device opens a WiFi access point named "tasmota-XXXXX", connect to that
- open `http://192.168.4.1` in a browser
- the device asks you for the WiFi name and password to connect to
- after entering those, the device will reconnect to that WiFi and disable its access point
- while doing that it should show you its new address in the browser, make a note of that
- in case that didn't happen, check your WiFi router for the address of the device

(3) Tasmota Setup
-----------------

- open the address from step (2) in a browser
- you should see the Tasmota web UI (a big "ON/OFF" text and a bunch of blue and one red button)
- click "Configuration"
- click "Configure Other"
- copy `{"NAME":"Gosund SP111 2","GPIO":[56,0,57,0,132,134,0,0,131,17,0,21,0],"FLAG":0,"BASE":18}` into the template input field
- tick the "Activate" checkbox
- click "Save"
- the device will restart, connect to it again
- the UI should now also contain text fields showing electrical properties, and the "Toggle" button should now actually work

(4) Calibration
---------------

- open the address from step (2) in a browser
- connect a purely resistive load with a known wattage, such as a conventional light bulb (not an LED or energy saving bulb)
- switch on power by clicking "Toggle" if needed
- verify that the "Power Factor" value is shown as 1 (or very close to 1); if it is lower the current load is not suited for calibration
- click "Console"
- enter the following commands one at a time and press enter:
```
AmpRes 3
VoltRes 3
EnergyRes 3
WattRes 3
FreqRes 3
SetOption21 1﻿
VoltageSet 230
```
- enter the command `PowerSet XXX` with XXX replaced by the wattage specified for the test load (e.g. "40" for a 40W light bulb)
- click "Main Menu"
- the main page now should show correct power readings with several decimals precision

(5) MQTT Broker Setup
---------------------

The only known way for high-frequency automatic readouts so far is polling over MQTT. This is not ideal and
needs additional setup unfortunately.

If you happen to have a MQTT Broker around already, skip to step (6), otherweise you need to set up one. The below assumes Mosquitto
is available packaged on your distribution, and doesn't configure any security, so only do this in your own
trusted network and switch it off when not needed.

- install the `mosquitto` package
- add a file `/etc/mosquitto/conf.d/listen.conf` with the following content:
```
listener 1883
allow_anonymous true
```
- start Mosquitto using `systemctl start mosquitto.service`

(6) MQTT Tasmota Setup
----------------------

Connect to the Tasmota device using a web browser, and open the MQTT configuration page via Configuration > Configure MQTT.
Enter the IP address of the MQTT broker into the "Host" field.

Note down the value shown right of the "Topic" label in parenthesis (typically something like "tasmota_xxxxxx"). This will be
needed later on in addressing the device via MQTT. You can also change the default value to something easier to remember, but
this has to be unique if you have multiple devices.

Press Save.

The device will restart and once it's back you should see output in its Console prefixed with "MQT".

(7) Verifying MQTT Communication
--------------------------------

This assumes you have the Mosquitto client tools installed, which are usually available as distribution packages.

You need two terminals to verify MQTT communication works as intended.
- In terminal 1, run `mosquitto_sub -t 'stat/<topic>/STATUS10'`
- In terminal 2, run `mosquitto_pub -t 'cmnd/<topic>/STATUS' -m '10'`

Replace `<topic>` with the value noted down in step (6).
Everytime you run the second command, you should see a set of values printed in the first terminal.

(8) Continuous Power Measurements
---------------------------------

- see scripts in https://volkerkrause.eu/2020/10/17/kde-cheap-power-measurement-tools.html 

(9) Switching WiFi Networks
---------------------------

Once connected to a WiFi network Tasmota will not let you get back to step (2) by default for security reasons,
without hard resetting the device (40sec button press). That however also removes all settings and the calibration.
If you need to move to a different network, there are less drastic options available though, but those can only
be taken inside the network you originally connected to:

- Under Configuration > Configure WiFi you can add details for a second WiFi access point. Those will be tried
alternatingly with the first configuration by default. This doesn't compromise security, but requires you to know
the details for the network you want to connect to.
- You can configure Tasmota to open an access point as in step (2) by default for a minute or so after boot, and
then trying to connect to the known configurations. This makes booting slower in known networks, and opens the
potential for hijacking the device, but it can be convenient when switching to unknown networks.
This mode can be enabled in the Console by the command `WifiConfig 2`, and disabled by the command `WifiConfig 4`.

For Tasmota version 11 the 40 sec button press reset can leave the device in a non-booting state, resetting from the
Console using `Reset 1` doesn't have that problem, but has to be done before disconnecting from the known WiFi as well.

(10) Recovering non-booting devices
-----------------------------------

With Tasmota 11 you can end up in a non-booting state by merely resetting the device using the 40 sec button press.
This is not permanently damaging the device, but can be fixed with reflashing via a serial adapter.

The basic process is described in https://tasmota.github.io/docs/Getting-Started/, the PCB layout of the
Gosund SP 111 can be seen on https://templates.blakadder.com/gosund_SP111_v1_1.

In order for this to work, you need to connect GPIO0 (second pin on bottom left in the above image) to GND
**before** powering up (ie. before connecting USB). The device LEDs (red and blue) are a useful indicator
whether you ended up in the right boot mode, red flashing quickly or red and blue being on is wrong, just red being
on is correct. Once in that state the connection can be removed (e.g. if you just hold a jumper cable to the pin),
it remains in the right mode until a reboot.

Most importantly: **DO NOT CONNECT THE DEVICE TO MAIN POWER**! That would be life-threatening, the entire flashing
process in solely powered from 3.3V supplied by the serial adapter. Do not do any of this without having read
https://tasmota.github.io/docs/Getting-Started/.
