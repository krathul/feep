<!--
SPDX-FileCopyrightText: 2021 KDE e.V. <https://ev.kde.org/>

SPDX-License-Identifier: CC-BY-SA-4.0
-->

The main advantage of this setup is that you do not have to install an additional program on the system under test (SUT) and therefore you do not create an additional load which has to be subtracted from the test result (CPU, RAM, HDD, power consumption).

Moreover, this setup allows one to test software on systems that do not support particular automation programs (e.g., on a tablet, smartphone, or Apple computer, or a company computer where nothing else may be installed). However, a system logfile must still be written on the SUT so that the load on the system can be monitored.

-   Test computer (with software to test), USB cable, Arduino board, 3 x Wire, USB to Serial Adapter, USB cable, GNU/Linux computer (workload generator).
-   Used the two boards:
    -   Arduino Pro Micro (ATmega32U4): <https://www.sparkfun.com/products/12640>
    -   and USB to Serial Adapter: <https://www.pololu.com/product/1308>, <https://www.adafruit.com/product/3309>
-   For the Arduino board: any other board can be used that acts as USB HID (all ATmega32U4 boards). For USB-to-Serial Adapter: actually any other should work too. I connected both boards with 3 wires/plugs via RX -> TX, TX -> RX, Gnd -> Gnd.
-   The Arduino software (keyMouSerialeinzeln9b.ino) has to be run on the Arduino board. After uploading the software to the Arduino board, this is plugged into the test computer as a mouse/keyboard replacement.
-   The second program (KeyboardUSB_improved6.pde) runs on a LINUX computer with Processing (<https://processing.org/>) as interpreter. When the Processing software has been started, the test computer can be operated via the keyboard and mouse of the LINUX computer.
-   Record starts after pressing Ctrl+Shift+1 and stops again after pressing Ctrl+Shift+1. The recording is now rudimentarily stored in a logfile keystrokes.txt in the same folder as the Processing program.
-   Playing (PLAY) the last recording works with Ctrl+Shift+3.

Any other Single Board Computer could work instead of an Arduino board: either you can make an output port out of an existing USB (input) port or you have to connect an additional breakout board (e.g., <https://www.adafruit.com/product/1501>).

German:

-   Testrechner (mit zu testender Software), USB-Kabel, Arduino Board, 3 x Draht, USB to Serial Adapter, USB-Kabel, LINUX-Rechner (Lasttreiber)
-   Genutzt habe ich die beiden Boards:
    -   Arduino Pro Micro (ATmega32U4): <https://www.sparkfun.com/products/12640>
    -   und USB to Serial Adapter: <https://www.pololu.com/product/1308>, <https://www.adafruit.com/product/3309>
-   Als Arduino-Board kann jedes andere verwendet werden, das als USB-HID auftreten kann (alle ATmega32U4-Boards) und als USB-to-Serial-Adapter sollte eigentlich jeder andere auch gehen. Beide Boards habe ich mit 3 Drähten/Steckern über RX -> TX, TX -> RX, Gnd -> Gnd verbunden.
-   Die Software (ino) muss zum einen auf das Arduino-Board gespielt werden. Nach dem Hochspielen der Software auf das Arduino-Board, wird das als Mouse/Tastatur-Ersatz in den Testrechner eingesteckt. Das zweite Programm (pde) läuft auf einem LINUX-Rechner mit Processing (<https://processing.org/>) als Interpreter. Wenn die Processing-Software gestartet wurde, kann der Testrechner über die Tastatur und Mouse des LINUX-Rechners bedient werden.
-   Aufzeichnen (Record) startet nach Knopfdruck Ctrl+Shift+1 und stoppt auch wieder nach Ctrl+Shift+1. Die Aufzeichnung landet jetzt rudimentär in einem Logfile keystrokes.txt  im gleichen Ordner, wie das Processing-Programm liegt.
-   Abspielen (PLAY) der letzten Aufzeichnung funktioniert mit Ctrl+Shift+3.

