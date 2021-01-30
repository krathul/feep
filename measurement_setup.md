# Measurement setup

The measurement setup consists of a computer as reference system, an energy meter for measuring energy consumption of the computer, and software to automate the usage scenario and record and process the measured data.

The setup described here follows the specifications from the [Blue Angel Basic Award Criteria for Resource and Energy-Efficient Software Products](https://produktinfo.blauer-engel.de/uploads/criteriafile/en/DE-UZ%20215-202001-en-Criteria-2020-02-13.pdf)

## Energy meter

One of the remmonded devices is the [GUDE Expert Power Control 1202](https://www.gude.info/en/power-distribution/switched-metered-pdu/expert-power-control-1202-series.html). It provides plugs for powering the computer and measures the current during operation. The device can be controlled and read via cabled Ethernet. There is a web-based user interface, a [REST API](http://wiki.gude.info/EPC_HTTP_Interface), and the device supports various protocols such as SNMP or syslog.

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

## Measurement of system performance indicators

During the energy measurement we also need to record a set of performance indicators: processor utilisation, RAM utilisation, hard disk activity and network traffic).

Tool candidates:

* [Collectl](http://collectl.sourceforge.net/)

## Measurement process

The measurement process is defined in Appendix A of the [Basic Award Criteria](https://produktinfo.blauer-engel.de/uploads/criteriafile/en/DE-UZ%20215-202001-en-Criteria-2020-02-13.pdf). It requires to record energy data and performance indicators with a granularity of 1 second and log it so it can be processed and average values can be calculated.

We might want to look into tools such as [Prometheus](https://prometheus.io/) to gather the data.
