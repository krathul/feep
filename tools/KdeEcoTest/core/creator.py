import json
import os
import signal
import time
import subprocess
import dbus

from pynput import keyboard, mouse
from pynput.keyboard import Key

from .constants import KEYS_MAP, OPTIMIZED_KEYS_MAP

windows_x = 0
windows_y = 0
window_defined = False
writeMousePosToFile = False
writeKeyboardKeysToFile = False
writeMouseOnce = False
win_id = 0
keys_buffer = []

clickForDrag = False
dragStartRecorded = False
dragEndRecorded = False


outputFilename = "testscript.txt"


def defineWindow(test_scirpt):
    global win_id

    # get application origin coordinates
    KWin_bus = dbus.SessionBus()
    KWin_proxy = KWin_bus.get_object('org.kde.KWin', '/KWin')
    win_id = KWin_proxy.queryWindowInfo(dbus_interface = 'org.kde.KWin')['uuid']
    #print(KWin_proxy.getWindowInfo(win_id, dbus_interface = 'org.kde.KWin')['uuid'])

    global win_location
    win_location = xdo.get_window_location(win_id)

    global window_defined
    window_defined = True

    global win_size
    win_size = xdo.get_window_size(win_id)

    # SetWindowToOriginalSize will need to be used, but at the moment I do not know where. It has to be written because KdeEcoTest has to be applied on the same windows size than the original tested window.
    global outputFilename
    outputFilename = test_scirpt
    file1 = open(outputFilename, "a")
    file1.write("# Original window properties\n")
    file1.write("moveWindowToOriginalLocation {0},{1}\n".format(win_location.x,win_location.y))
    file1.write("setWindowToOriginalSize {0},{1}\n\n".format(win_size.width, win_size.height))
    file1.close()


def addClick():
    if window_defined == False:
        print("To add click mouse coordinates, first define which application is tested.")
        print("Enter the dw command (defined window) and click on the application.")
    else:
        print("Mouse click is now added to the end of the KdeEcoTest output file.")

        global writeMousePosToFile
        writeMousePosToFile = True


def addKeyboardKeys():
    if window_defined == False:
        print("To add keyboard keys, first define which application is tested.")
        print("Enter the dw command (defined window) and click on the application.")
    else:
        print("Keyboard keys are now added to the end of the KdeEcoTest output file.")

        global writeKeyboardKeysToFile
        writeKeyboardKeysToFile = True


def stopKeyboardKeys():
    print("Keyboard keys are not added anymore to the output file.")
    global writeKeyboardKeysToFile
    writeKeyboardKeysToFile = False


def stopClick():
    print("Mouse clicks are not added anymore to the output file.")
    global writeMousePosToFile
    writeMousePosToFile = False


def scrollup():
    saveRecordedKeys()
    file1 = open(outputFilename, "a")
    file1.write("scrollup\n")
    file1.write("sleep 2\n")
    file1.write("\n")
    file1.close()


def scrolldown():
    saveRecordedKeys()
    file1 = open(outputFilename, "a")
    file1.write("scrolldown\n")
    file1.write("sleep 2\n")
    file1.write("\n")
    file1.close()


def writeToScreen():
    global windows_x
    global windows_y
    print("Write to the screen, enter you text.")
    textInput = input()
    print("Text entered :" + textInput)
    file1 = open(outputFilename, "a")
    file1.write("# Comment\n")
    file1.write('write "' + textInput + '"' + "," + str(windows_x) + "," + str(windows_y) + "\n")
    file1.write("sleep 2\n")
    file1.write("\n")
    file1.close()


def writeMessageToLog():
    print("Write a message to the log file, enter you text.")
    textInput = input()
    print("Text entered :" + textInput)
    file1 = open(outputFilename, "a")
    file1.write("# Write message to the log.\n")
    file1.write('writeMessageToLog "' + textInput + '"\n')
    file1.write("\n")
    file1.close()
    print("Log timestamp command written to the sript.")


# get input arguments
"""
parser = argparse.ArgumentParser()
parser.add_argument(
    "--outputFilename", required=True, help="Test script to be used with KdeEcoTest."
)
args = parser.parse_args()
"""


def exitApp():
    print("Program aborted.")
    os.kill(os.getpid(), signal.SIGTERM)


def saveRecordedKeys():
    global keys_buffer
    if len(keys_buffer) == 0:
        return
    file1 = open(outputFilename, "a")
    file1.write("# Write recorded keys.\n")
    file1.write("writeRecordedKeys ")
    optmized_keys_buffer = []
    for key in keys_buffer:
        if key in OPTIMIZED_KEYS_MAP:
            optmized_keys_buffer.append(OPTIMIZED_KEYS_MAP[key])
        else:
            optmized_keys_buffer.append(key)
    keys_buffer = []
    file1.write(json.dumps(optmized_keys_buffer))
    file1.write("\nsleep 2\n")
    file1.write("\n")
    file1.close()


def windowAlive(window_id):
    try:
        subprocess.check_output(["xdotool", "getwindowname", f"{window_id}"], stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False


def on_press(key):
    try:
        if win_id and windowAlive(win_id) == False:
            exitApp()

        xdo = Xdo()
        curr_window = xdo.get_window_at_mouse()
        if curr_window != win_id:
            return

        global writeKeyboardKeysToFile
        if key == Key.esc:
            if writeKeyboardKeysToFile:
                stopKeyboardKeys()
                saveRecordedKeys()
            else:
                exitApp()

        else:
            if hasattr(key, "char"):
                keys_buffer.append(key.char)

            elif key._name_ in KEYS_MAP:
                keys_buffer.append(key._name_)

            else:
                return

    except AttributeError as e:
        print(e)
        print("special key {0} pressed".format(key))


def on_click(x, y, button, pressed):
    saveRecordedKeys()
    global writeMousePosToFile
    global writeMouseOnce
    global win_id

    if win_id and windowAlive(win_id) == False:
        exitApp()

    global clickForDrag
    global dragStartRecorded
    global dragEndRecorded
    global windows_x
    global windows_y

    if writeMousePosToFile or clickForDrag:
        if button == mouse.Button.left:
            if pressed:
                if (x > win_location.x + win_size.width) or (x < win_location.x) or (y > win_location.y + win_size.height) or (y < win_location.y + win_size.height):
                    print("Click outside window, do not record click")
                    return

                windows_x = x - win_location.x
                windows_y = y - win_location.y

                print(" a click here")
                print("for drag: ", clickForDrag)

                if clickForDrag:
                    print("click for drag")
                    if dragStartRecorded == False:
                        dragStartRecorded = True
                        print("Drag start recorded")

                    elif dragEndRecorded == False:
                        dragEndRecorded = True
                        print("Drag end recorded")

                else:
                    print("mouse click position added to the file")
                    file1 = open(outputFilename, "a")
                    clickOnMsgStr = "click {0},{1}".format(windows_x, windows_y)
                    sleepMsgStr = "sleep {0}".format(2)
                    file1.write("# Click on\n")
                    file1.write(clickOnMsgStr + "\n")
                    file1.write(sleepMsgStr + "\n")
                    file1.write("\n")
                    print("# Click on")
                    print(clickOnMsgStr)
                    print(sleepMsgStr)

                if writeMouseOnce:
                    writeMousePosToFile = False
                    writeMouseOnce = False
                else:
                    # Using asynchronous is tricky, I am wondering how we could use the while True: loop to get its Enter command print. Meanwhile I am writting this fudge:
                    print("Enter Your command:\n")


# select start point and end point with mouse clicks and store them in a file
def addDrag():
    if window_defined == False:
        print("To add drag mouse coordinates, first define which application is tested.")
        print("Enter the dw command (defined window) and click on the application.")
    else:
        print("Mouse drag is now added to the end of the KdeEcoTest output file.")

        global clickForDrag
        clickForDrag = True

        print("Click on the start point of the drag.")
        global dragStartRecorded
        while dragStartRecorded == False:
            print("waiting for start point...")
            time.sleep(1)
            continue
        dragStartRecorded = True

        start_x = windows_x
        start_y = windows_y

        print("Click on the end point of the drag.")
        global dragEndRecorded
        while dragEndRecorded == False:
            print("waiting for end point...")
            time.sleep(1)
            continue
        dragEndRecorded = True

        end_x = windows_x
        end_y = windows_y

        file1 = open(outputFilename, "a")
        file1.write("# Drag\n")
        file1.write("dragMouse {0},{1} to {2},{3}\n".format(start_x, start_y, end_x, end_y))
        file1.write("sleep 2\n")
        file1.write("\n")
        file1.close()

        print("Drag coordinates added to the file.")
        print("Enter Your command:\n")


def createTestScript(test_script):
    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()

    keyboard_listener = keyboard.Listener(on_press=on_press)
    keyboard_listener.start()

    print("KdeEcoTestCreator helps to edit KdeEcoTest script files.")
    print("Commands:")
    print("dw: define window.")
    print("asc: add single click.")
    print("ac: add clicks.")
    print("sc: stop add clicks.")
    print("ws: write to the screen.")
    print("wmtl: write message to log.")
    print("asu : after scroll up ")
    print("asd : after scroll down")
    print("drg: add drag.")
    print("ak: add keyboard keys.")
    print("sk: stop add keyboard keys.")
    print("\n")

    print("To begin with, click on the application you want the script to be written for.")
    defineWindow(test_script)

    while True:
        global writeMouseOnce
        if writeMouseOnce:
            continue

        print("Enter your command: ")
        commandStr = input()

        if commandStr == "dw":
            defineWindow(test_script)
        elif commandStr == "ws":
            writeToScreen()
        elif commandStr == "ac":
            addClick()
        elif commandStr == "sc":
            stopClick()
        elif commandStr == "ak":
            addKeyboardKeys()
        elif commandStr == "sk":
            stopKeyboardKeys()
        elif commandStr == "asc":
            writeMouseOnce = True
            addClick()
        elif commandStr == "drg":
            addDrag()
        elif commandStr == "asu":
            scrollup()
        elif commandStr == "asd":
            scrolldown()
        elif commandStr == "wmtl":
            writeMessageToLog()
        elif commandStr == "q":
            os.kill(os.getpid(), signal.SIGTERM)
        else:
            print("Command unknown.")
