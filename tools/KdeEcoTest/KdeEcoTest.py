import re
import argparse
import os
from pynput.mouse import Listener
from pynput import mouse
from pynput import keyboard
from pynput.keyboard import Key
from xdo import Xdo
import time
import signal
from datetime import datetime as dt
import os.path

window_defined = False
writeMousePosToFile = False
testIsRunning = True

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key))
        if key == Key.f1:
            global testIsRunning
            if testIsRunning == True:
                testIsRunning = False
                print("The testing program is on pause.")
            else:
                testIsRunning = True
                print("The testing program is running.")
        if key == Key.f2:
            print("Program aborted.")
            os.kill(os.getpid(), signal.SIGTERM)

    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def writeToLog(logFileName, logStr):
    file1 = open(logFileName, 'a')
    file1.write(logStr)
    file1.write("\n")
    file1.close()


def defineWindow():
    ## get application origin coordinates
    global xdo
    xdo = Xdo()
    global win_id
    win_id = xdo.select_window_with_click()

    global win_location
    win_location = xdo.get_window_location(win_id)
    print(win_location.x)
    
    print(win_location.y)
    global window_defined
    window_defined = True

    global win_size
    win_size = xdo.get_window_size(win_id)
    print(win_size.width)
    print(win_size.height)

#get input arguments
parser = argparse.ArgumentParser()
parser.add_argument("--inputFilename", required=True, help = "Test script to be used with KdeEcoTest.")
parser.add_argument("--testLogFilename", required=False, help = "Test log filename")
args = parser.parse_args()
intputFilename = args.inputFilename

#get log filename, create a default one if none provided
now = dt.now()
testLogFilename = "KdeEcoLogFile_" + now.strftime("%Y-%m-%d_%H-%M-%S")
print(testLogFilename)
if args.testLogFilename is not None:
    testLogFilename = args.testLogFilename

print("--")
print(intputFilename)
print(testLogFilename)
print("--")

#Test if intputFilename exists
if os.path.exists(intputFilename) == False:
    print("Input filename {0} has not been found.".format(intputFilename))
    os.kill(os.getpid(), signal.SIGTERM)

listener = keyboard.Listener(
    on_press=on_press)
listener.start()

#get the location and size of the application to test
print("Click on the application you want to test.")
defineWindow()

#read KdeEcoTest input file line by line and execute the test
file1 = open(intputFilename, 'r')
count = 0
line = file1.readline()
print(line)

while line != "":
    if testIsRunning == True:
        strMatch = re.search('click (\d*),(\d*)',line.lower())
        if strMatch:
            x = strMatch.group(1)
            y = strMatch.group(2)
            xdo.move_mouse(win_location.x + int(x), win_location.y + int(y))
            xdo.click_window(win_id, 1)


        strMatch = re.search('sleep ([\d\.]*)',line.lower())
        if strMatch:
            sleep_time = strMatch.group(1)
            time.sleep(float(sleep_time))

        strMatch = re.search('write "([^\"]*)",(\d*),(\d*)',line.lower())
        if strMatch:
            stringToWriteToScreen = strMatch.group(1)
            string_x = strMatch.group(2)
            string_y = strMatch.group(3)
            xdo.move_mouse(win_location.x + int(string_x), win_location.x + int(string_y))

            xdo.focus_window(win_id)
            #xdo.wait_for_window_focus(win_id, 1)
            os.system('xdotool type --window {0} --delay [500] \"{1}\" '.format(win_id,stringToWriteToScreen))

        strMatch = re.search('moveWindowToOriginalLocation (\d*),(\d*)',line)
        if strMatch:
            print("Move tested window to original location.")
            origWin_x = strMatch.group(1)
            origWin_y = strMatch.group(2)
            os.system('xdotool windowmove {0} {1} {2}'.format(win_id,origWin_x,origWin_y))
            #xdo.move_window(win_id, origWin_x, origWin_y)

        strMatch = re.search('setWindowToOriginalSize (\d*),(\d*)',line)
        if strMatch:
            print("Set tested window to original size.")
            origWin_width = strMatch.group(1)
            origWin_height = strMatch.group(2)
            os.system('xdotool windowsize {0} {1} {2}'.format(win_id,origWin_width,origWin_height))

        strMatch = re.search('key (.*)',line)
        if strMatch:
            print("Send key.")
            keyStr = strMatch.group(1)
            print(keyStr)
            os.system('xdotool key {0}'.format(keyStr))

        strMatch = re.search('writeTimestampToLog "([^\"]*)"',line)
        if strMatch:
            print("Write timestamp to log.")
            now = dt.now()
            timestampStr = now.strftime("%a %m %y")
            print('Timestamp:', timestampStr)
            file1 = open(outputFilename, 'a')
            file1.write("# Write message to the log.\n")
            file1.write("writeMessageToLog \"" + textInput + "\"\n")
            file1.write("\n")
            file1.close()



        count += 1
        lineStr = "Line{:0>3d}: {}".format(count, line.strip())
        print(lineStr)
        if line.strip() != "":
            now = dt.now()
            writeToLog(testLogFilename,now.strftime("%Y-%m-%d_%H-%M-%S " + lineStr))

        line = file1.readline()


