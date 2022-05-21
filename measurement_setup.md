# Measurement setup

The measurement setup consists of a computer as reference system, an energy meter for measuring energy consumption of the computer, and software to automate the usage scenario and record and process the measured data.

The setup described here follows the specifications from the [Blue Angel Basic Award Criteria for Resource and Energy-Efficient Software Products](https://produktinfo.blauer-engel.de/uploads/criteriafile/en/DE-UZ%20215-202001-en-Criteria-2020-02-13.pdf)

## Energy meter

### GUDE Expert Power Control 1202

One of the recommended devices is the [GUDE Expert Power Control 1202](https://www.gude.info/en/power-distribution/switched-metered-pdu/expert-power-control-1202-series.html) ([manual](https://gude-systems.com/app/uploads/2022/05/manual-epc1202-series.pdf)). It provides plugs for powering the computer and measures the current during operation. The device can be controlled and read via cabled Ethernet. There is a web-based user interface, a [REST API](http://wiki.gude.info/EPC_HTTP_Interface), and the device supports various protocols such as SNMP or syslog.

There is a script available to read data from the device via SNMP: https://gitlab.rlp.net/green-software-engineering/mobiles-messgerat

Here are some notes how to make it work (quick and dirty):

The script uses `snmpget` to read out measurement data via SNMP. On Ubuntu it can be installed with `apt install snmp`.

To install the necessary SNMP info you also need to install the package `snmp-mibs-downloader` on Ubuntu.

In the web interface of the measuring device you need to enable SNMP. Go to the Configuration tab, choose "Protocols" and then "SNMP" and check the checkboxes "Enable SNMP options". This enables SNMP v1 which is used by the measurement script.

You also need to download the SNMP information for the measurement device. Click the link "MIB table" to show it and then save it to your local machine as `GUADES-EPC1202-MIB.txt`. Store it to `/usr/share/snmp/mibs` and set the environment variable to activate it: `export MIBS=+GUADES-EPC1202-MIB`.

To configure the script `get_energy_utilization.py`, which reads the measurement data and writes it to a file, you have to set some more enviornment variables:

* `LOGFILE`: Set it to the name of the file, where the measurement data is stored.
* `IP`: Set it to the host name or IP address of the measurement device
* `AMPERE_ADDRESS`: Set it to the SNMP object id of the current measurement. You can take it from the MIB file. Take OID of `epc1202Current`. Append `.1` to get the value. This results in something like: `export AMPERE_ADDRESS=1.3.6.1.4.1.28507.43.1.5.1.2.1.5.1`.
* `VOLTAGE_ADDRESS`: Set it to the SNMP object id of the voltage measurement. You can take it from the MIB file. Take OID of `epc1202Voltage`. Append `.1` to get the value.
* `POWERFACTOR_ADDRESS`: Take the OID of `epc1202PowerFactor` from the MIB file. Append `.1` to get the value.

There seems to be an incompatibility in the script. Change the last lines of the `getSNMP` method to

    fields=line.split(": ")
    return int(fields[1].split()[0])

Then run the script. It will print the measurments to standard output and write them to the log file. Stop it with CTRL-C, when the measurement is done.

The results looks like this:
```
Zeit;Wert 1-avg[W]
2022-05-21 17:52:22.838772; 23.760564
2022-05-21 17:52:24.306634; 23.656351
2022-05-21 17:52:25.502201; 23.70107
2022-05-21 17:52:26.774169; 23.70107
2022-05-21 17:52:27.837169; 23.656351
2022-05-21 17:52:28.871263; 23.625252
2022-05-21 17:52:29.917944; 23.656351
2022-05-21 17:52:31.364232; 23.70107
2022-05-21 17:52:33.329414; 23.656351
2022-05-21 17:52:34.915585; 23.656351
2022-05-21 17:52:35.986060; 23.80548
2022-05-21 17:52:37.022003; 23.729328
2022-05-21 17:52:39.152300; 23.639952
2022-05-21 17:52:40.740454; 23.656351
2022-05-21 17:52:41.804313; 23.760564
2022-05-21 17:52:43.067764; 23.7156
```

### Other devices

As an alternative it might be possible to [repurpose cheap switchable power plugs as measurement devices](https://volkerkrause.eu/2020/10/17/kde-cheap-power-measurement-tools.html)

## Reference system

One of the recommended reference systems is the Fujitsu Esprimo P920 Desktop-PC proGreen selection (Intel Core i5-4570 3,6GHz, 4GB RAM, 500GB HDD). Ubuntu 18.04. runs fine on it and can be used for measurements.

## Test automation

We need an automation tool which can run the standard usage scenarios in a way which doesn't need human intervention, so it can be run repeatedly in a well-defined way to provide accurate measurements.

There are some candidates for tools which might meet the requirements:

* [Actiona](https://github.com/Jmgr/actiona)
* [xdotool](https://github.com/jordansissel/xdotool)
* [Atbswp](https://github.com/RMPR/atbswp)
* [SikuliX](https://github.com/RaiMan/SikuliX1)

There might be more. We need to assess them and come up with a working solution.

Most of these tools use X11-specific features and thus do not work on Wayland systems. There are a few possible approaches here:
* [The XDG RemoteDesktop portal](https://docs.flatpak.org/en/latest/portal-api-reference.html#gdbus-org.freedesktop.portal.RemoteDesktop)
* Various Wayland protocols (https://github.com/swaywm/wlr-protocols/blob/master/unstable/wlr-virtual-pointer-unstable-v1.xml, https://api.kde.org/frameworks/kwayland/html/classKWayland_1_1Client_1_1FakeInput.html). Support varies between compositors.
* [libinput user devices](https://lwn.net/Articles/801767/)

## Measurement of system performance indicators

During the energy measurement we also need to record a set of performance indicators: processor utilisation, RAM utilisation, hard disk activity and network traffic.

Tool candidates:

* [Collectl](http://collectl.sourceforge.net/)

## Measurement process

The measurement process is defined in Appendix A of the [Basic Award Criteria](https://produktinfo.blauer-engel.de/uploads/criteriafile/en/DE-UZ%20215-202001-en-Criteria-2020-02-13.pdf). It requires to record energy data and performance indicators with a granularity of 1 second and log it so it can be processed and average values can be calculated.

We might want to look into tools such as [Prometheus](https://prometheus.io/) to gather the data.

## Measurement reports

There is a tool available from Umwelt-Campus Birkenfeld, which generates reports from measurement data, called OSCAR (Open
Source Software Consumption Analysis): [Running instance](https://oscar.umwelt-campus.de/), [Source Code](https://gitlab.umwelt-campus.de/y.becker/oscar-public).
