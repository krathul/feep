# KdeEcoTest | KdeEcoTestCreator

![KDE-ECO-TEST IMAGE](Kdeecotest.png)

`KdeEcoTest` and `KdeEcoTestCreator` are Python-based tools designed for reproducing computer actions by simulating keyboard and mouse acitivity.

Contents
========
* [Why?](#why)
* [Installation](#installation)
* [Usage](#usage)
* [Want to contribute?](#want-to-contribute)

### Why?

A Standard Usage Scenario reflects the typical functions of an application and is central to measuring the energy consumption of software in a reproducible way.

`KdeEcoTest` helps to create a script which simulates the activities of a normal user in order to create a Standard Usage Scenario. `KdeEcoTest` also runs those scripts to automate emulation of user behavior in order to measure energy consumption of an application while in use.

`KdeEcoTest` is a cross-platform and CLI based Python tool which is built using `xdotool`.

### Usage

#### Clone & Setup the virtual environment

```bash
$ git clone https://invent.kde.org/teams/eco/feep.git
$ cd feep/tools/KdeEcoTest/

#Do these steps only if you are on KDE plasma
$ mkdir -p externals/kdotool
$ git clone https://github.com/jinliu/kdotool.git externals/kdotool
$ make

$ pip install pipenv
$ pipenv install
$ pipenv shell
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
