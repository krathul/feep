# Modify Actiona script to adapt click coordinates to different screen resolutions
import re
import argparse
import os
from pynput.mouse import Listener
from pynput import mouse
from pynput import keyboard
from pynput.keyboard import Key
import argparse
from xdo import Xdo

window_defined = False
writeMousePosToFile = False


def defineWindow():
    ## get application origin coordinates
    xdo = Xdo()
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

    file1 = open(outputFilename, 'a')
    file1.write("# Original window properties\n")
    file1.write("moveWindowToOriginalLocation {0},{1}\n".format(win_location.x,win_location.y))
    file1.write("setWindowToOriginalSize {0},{1}\n\n".format(win_size.width,win_size.height))
    file1.close()


def addClick():
    if window_defined == False:
        print("To add click mouse coordinates, first define which application is tested.")
        print("Enter the dw command (defined window) and click on the application.")
    else:    
        print("Every mouse click are now added to the end of the KdeEcoTest output file.")
        
        print("Add click at " + str(win_location.x) + "," + str(win_location.y))
        global writeMousePosToFile
        writeMousePosToFile = True

def stopClick():
        print("Mouse clicks are not added anymore to the output file.")  
        global writeMousePosToFile
        writeMousePosToFile = False
    
def writeToScreen():
    print("Write to the screen, enter you text.")
    textInput = input()
    print("Text entered :" + textInput)
    file1 = open(outputFilename, 'a')
    file1.write("# Comment\n")
    file1.write("write \"" + textInput + "\"" + "," + str(windows_x) + "," + str(windows_y) + "\n")
    file1.write("sleep 2\n")
    file1.write("\n")
    file1.close()
    


#get input arguments
parser = argparse.ArgumentParser()
parser.add_argument("--outputFilename", required=True, help = "Test script to be used with KdeEcoTest.")
args = parser.parse_args()
outputFilename = args.outputFilename 


def on_click(x, y, button, pressed):
    if writeMousePosToFile:
        print("tttttttttttttttttttttt1")
        if button == mouse.Button.left:
            if pressed:
                print("test")
                print(x)
                print(win_location.x)
                #+ win_size.width)

                if ((x > win_location.x + win_size.width) or (y > win_location.y + win_size.height)):
                    print("Click outside window, do not record click")
                    return

                print("mouse click position added to the file")
                global windows_x
                windows_x = x - win_location.x
                print(windows_x)
                global windows_y
                windows_y = y - win_location.y
                print("win_location: ")
                print(win_location)
                print("test: " + outputFilename)
                file1 = open(outputFilename, 'a')
                clickOnMsgStr = 'click {0},{1}'.format(windows_x, windows_y)
                sleepMsgStr = 'sleep {0}'.format(2)
                file1.write("# Click on\n")
                file1.write(clickOnMsgStr + "\n")
                file1.write(sleepMsgStr + "\n")
                file1.write("\n")
                print(clickOnMsgStr + "\n")
                print(sleepMsgStr + "\n")
                print("\n")

    
listener = mouse.Listener(
    on_click=on_click)
listener.start()    


print("KdeEcoTestCreator helps to edit KdeEcoTest script files.")
print("Commands:")
print("dw: define window.")
print("ac: add clicks.")
print("sc: stop add clicks.")
print("ws: write to the screen.")
print("\n")

print("To begin with, click on the application you want the script to be written for.")
defineWindow()
print("window_defined: ")
print(window_defined)
print("\n")


while True:
    print("Enter your command: ")
    commandStr = input()
    
 
    if commandStr == "dw":
        defineWindow()
    elif commandStr == "ws":
        writeToScreen()
    elif commandStr == "ac":
        addClick()
    elif commandStr == "sc":
        stopClick()
    elif commandStr == "q":
        os._exit()
    else:
        print("Command unknown.")
        
        















 
