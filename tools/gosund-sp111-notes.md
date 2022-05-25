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
- open http://192.168.4.1 in a browser
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
- copy '{"NAME":"Gosund SP111 2","GPIO":[56,0,57,0,132,134,0,0,131,17,0,21,0],"FLAG":0,"BASE":18}' into the template input field (without the enclosing '')
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
AmpRes 3
VoltRes 3
EnergyRes 3
WattRes 3
FreqRes 3
SetOption21 1﻿
VoltageSet 230
- enter the command "PowerSet XXX" with XXX replaced by the wattage specified for the test load (e.g. "40" for a 40W light bulb)
- click "Main Menu"
- the main page now should show correct power readings with several decimals precision

(5) MQTT Broker Setup
---------------------

- TODO

(6) MQTT Tasmota Setup
----------------------

- TODO

(7) Verifying MQTT Communication
--------------------------------

- TODO

(8) Continuous Power Measurements
---------------------------------

- see scripts in https://volkerkrause.eu/2020/10/17/kde-cheap-power-measurement-tools.html 
