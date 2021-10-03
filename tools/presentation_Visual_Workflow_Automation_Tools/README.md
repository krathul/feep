# Overview for Some Visual Workflow Automation Tools

(These are the notes for my presentation on 2021-10-08.)

This overview collects some existing tools that could be used for “Visual Workflow Automation”.
For each tool it is described what it is (e. g. graphical tool, command line tool, library, ...), and what it can do.
It is also described how it works, how it is executed, and how it interfaces towards the test subject.

Descriptions are focused on Linux, e. g. whether it works with X, Wayland, RDP, VirtualBox, or whatever.

## Example

https://some.url/

* It is:
    - Library? Graphical? IDE? Targeted at? Small or large? Proprietary?
* It can:
    - Main features. Record? Play? Modify? Embedded scripting? Image detection? Verification?
* Interface to test subject:
    - How the test subject is controlled. X? D-Bus?
* It runs on:
    - Prerequisites for using this tool. Operating system? Hardware? Takes control of current desktop?

## xdotool

https://www.semicomplete.com/projects/xdotool

* It is:
    - A command line tool to give shell access to X.
    - Simplified interface to XTEST.
* It can:
    - Send keyboard and mouse events to windows.
    - Manipulate window and desktop properties.
* Interface to test subject:
    - via X.
* It runs:
    - On the same desktop as the test subject.
    - Linux

## Xnee

https://savannah.gnu.org/projects/xnee/

* It is:
    - A library to record and replay X input events.
    - A CLI and GUI frontend for the library.
* It can:
    - Record keyboard and mouse events to a file.
    - Compress mouse events.
    - Replay events from the file.
    - Replay to multiple X sessions.
* Interface to test subject:
    - via X.
* It runs:
    - On any system with access to the targeted X session.
    - Linux

## PyAutoGUI

https://pypi.org/project/PyAutoGUI/

* It is:
    - A Python library to control GUI applications.
* It can:
    - Send keyboard and mouse events to the test subject.
    - Make screen captures of the test subject.
        + Locate images in them. (With OpenCV support.)
* Interface to test subject:
    - via X (Linux version).
* It runs:
    - On the same desktop as the test subject, only on the primary screen.
    - Windows, Mac, Linux

## Atbswp

“Automate the boring stuff with Python” https://github.com/rmpr/atbswp

* It is:
    - A wxPython toolbar to record and play macros.
* It can:
    - Record and play keyboard and mouse events on the primary screen.
    - Save macros as python scripts.
* Interface to test subject:
    - via X (PyAutoGUI).
    - Wayland support announced.
* It runs:
    - On the same desktop as the test subject, only on the primary screen.
    - Windows, Linux

## Actiona

https://actiona.tools/

* It is:
    - A Qt GUI application for visual workflow automation.
    - A drag&drop editor for workflows.
* It can:
    - Send keyboard and mouse events.
    - Control flow with JavaScript.
* Interface to test subject:
    - via X.
* It runs on:
    - On the same desktop as the test subject.
    - Windows, Linux

## Sikulix

https://sikulix.com

* It is:
    - A Java GUI application for visual workflow automation.
    - A Java/JPython library to control GUI applications.
* It can:
    - Send keyboard and mouse events to the test subject.
    - Make screen captures of the test subject.
        + Do text and image recognition on them. (OpenCV https://opencv.org, Tesseract https://github.com/tesseract-ocr/)
    - Control flow with JPython logic.
    - Interact with the real user through dialog windows.
    - IDE with inline thumbnail display.
* Interface to test subject:
    - via interface classes. For Linux:
        - via X.
        - IRobot: RobotDesktop implementation in Java AWT
        - OsWindow: LinuxWindow implementation in xdotool
* It runs:
    - On the same desktop as the test subject (with the existing implementation).
    - Windows, Mac, Linux

## Squish

https://www.froglogic.com/squish/

* It is:
    - A proprietary suite for automatic GUI testing.
* It can:
    - Record and send keyboard and mouse events.
    - Record user interactions on GUI toolkit level or visual level.
    - Visual verification with image and text recognition.
* Interface to test subject:
    - via GUI toolkit or VNC.
* It runs:
    - Within the test subject or as VNC client.
    - Windows, Mac, Linux

## Eggplant Functional

http://docs.eggplantsoftware.com/ePF/gettingstarted/epf-getting-started-eggplant-functional.htm

* It is:
    - A proprietary suite for automatic GUI testing.
    - An IDE to write test scripts.
* It can:
    - Record and send keyboad and mouse events.
    - Record user interactions on visual level.
    - Locate text and images on the screen.
* Interface to test subject:
    - VNC or RDP.
* It runs:
    - As VNC or RDP client.
    - Windows, Mac, Linux

## Microsoft Power Automate Desktop / WinAutomation

https://flow.microsoft.com/en-us/desktop/
https://docs.microsoft.com/en-us/power-automate/desktop-flows/

* It is:
    - A proprietary suite for workflow automation (tendency to non-visual cloud services).
    - A drag&drop editor for “flows”
    - A library of high-level interfaces to other applications.
* It can:
    - Send keyboard and mouse events.
    - Locate images on the screen.
    - Process data in the cloud.
    - Manipulate system configuration.
* Interface to test subject:
    - Windows desktop.
* It runs:
    - On the same physical desktop as the test subject.
    - Windows

## PuloversMacroCreator

https://macrocreator.com

* It is:
    - An AutoHotkey GUI application for visual workflow automation.
    - An IDE to write AutoHotkey scripts.
    - A library of high-level interfaces to other applications.
* It can:
    - Record and play keyboard and mouse events.
    - Locate images on the screen.
* Interface to test subject:
    - AutoHotkey (Windows desktop)
* It runs:
    - On the same desktop as the test subject.
    - Windows
