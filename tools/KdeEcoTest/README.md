# KdeEcoTest
Contents
========
* [Why?](#why)
* [Installation](#installation)
* [Usage](#usage)
* [Want to contribute?](#want-to-contribute)

### Why?

A Standard Usage Scenario reflects the typical functions of an application and is central to measuring the energy consumption of software in a reproducible way.

`KdeEcoTest` helps to create a script which simulates the activities of a normal user in order to create a Standard Usage Scenario. `KdeEcoTest` also runs those scripts to automate emulation of user behavior in order to measure energy consumption of an application while in use.

`KdeEcoTest` is a cross-platform CLI based Python tool.

### Testing and Usage

#### Setup

```bash
$ git clone -b dev https://invent.kde.org/krathul/feep.git
$ cd feep/tools/KdeEcoTest/
$ pip install pipenv

#Do these steps only if you are on KDE plasma
$ mkdir -p externals/kdotool
$ git clone -b dev https://invent.kde.org/krathul/kdotool.git externals/kdotool
$ make

#Create environment and install dependencies
$ pipenv install
#Activate the environment
$ pipenv shell

#For running on X11 based systems, you need to additionally install python-libxdo and xdotools
$ pipenv install python-libxdo
#For installing xdotool check your package manager for info

```

KdeEcotest uses libevdev for reading and simulating events from input devices, and requires permission to read and write from /dev/input, /dev/uinput, /dev/console
This can be done by other modifying the permissions to the file or adding the user to the required groups

To grant permissions temporarily (Per login session)
```bash
$ sudo chmod +0666 /dev/uinput
$ sudo chmod -R +0666 /dev/input
$ sudo chmod +0666 /dev/console
```

For permanently giving permissions, you can add the user to groups input and tty (tty group doesn't have permissions to read from /dev/console, you have to give it permission manually), for /dev/uinput, you will have to add new rules.
```bash
$ sudo usermod -aG input,tty $USER
```

#### Create new script 

```bash
$ python3 KdeEcoTest.py create <SCRIPT_NAME>
```
- To abort the program : Press Esc
- A round mouse pointer appears. Click on the window you want to test. Now, you can use these options provided by `KdeEcoTest` to simulate actions and create a test script.

```shell
Commands:
dw: define window.
ac: add clicks.
sc: stop add clicks.
ws: write to the screen.
wtl: write test timestamp to log.
wmtl: write message to log.
```

#### Run a script

`KdeEcoTest` automates the actions stored in the created scripts.

- To run `KdeEcoTest` script:
```bash
$ python3 KdeEcoTest.py run <SCRIPT_NAME>
```
- To abort the program: Press Esc

### Want to contribute?

Before contributing, fork the repository and make an MR when you fix the issue.

Contribute in the following ways:

#### To-Do's

See "KdeEcoTest" Issues at this repository's [issue tracker](https://invent.kde.org/teams/eco/feep/-/issues).

Ask questions at the Matrix room [KDE Energy Efficency](https://matrix.to/#/#energy-efficiency:kde.org).
