1- What are KdeTestCreator and KdeTest ?
KdeTestCreator and KdeTest are tools which together aim at reproducing actions on a computer.
They have been created in order to produce energy consumption measurements. Simulating human usage of a computer through a long period, they help to measure what the applications energy consomptions are and spot where they can be improved.

2- Packages and modules required
In order to run, KdeEcoTest and KdeEcoTestCreator require python-libxdo and pynput. Using your package manager you need to install pip, then you can use pip to install the modules.
 - pip install python-libxdo
 - pip install pynput
 You also need to install the package xdotool using your prefered package manager.

3- KdeEcoTestCreator usage
KdeEcoTestCreator creates the testing scrip that will be used by KdeEco test.
To start KdeEcoTestCreator, type the following command:
  python3 KdeEcoTestCreator.py --outputFilename KdeEcoTestScript.txt
A round mouse pointer appears. Click on the application you want to test.
Open testOutputScript.txt into Kate (turn on Kate automatic file reloading).
Command prompt invites you to enter one of the available command.
  ac: adds comment line, click position and pause at the end of testOutputScript.txt.
     eg:
     # Click on the GCompris configuration icon
     click 631,760
     sleep 2
  sc: stops click recording
  ws: records text string that will be added at the position x,y
     eg:
     write "text to be added",x,y


4- KdeEcoTest usage
KdeEcoTest script files to execute actions in order to test computer applications. These can be created using KdeEcoTestCreator or by hand.
To start the test, enter the following command:
  python3 KdeEcoTest.py --inputFilename KdeEcoTestScript.txt
To pause the test, press F1.
To abort the program, press F2


To do:
- add writing timestamp log function.
- add writing action name log function.
- While in pause, when modifiying the input script, KdeEco test is still recording any key entry.
Do we need to add an additional focus test on the application tested to avoid this. This would allow to use space instead of F1 key to pause.
- Try to find a mecanisme to use space and esc instead of f1 and f2 into KdeEcoTest to make the test application more user friendly.
- Add a comment mécanisme, if a line starts with # should be ignored
- Choose an extension that would allow kate to use its comment mecanism adding # easilly (ctrl-D)
- Find a way to avoid using ctrl-s in kate to avoid warning messages about external saving.
- Add a goto mecanism.
- Add a counter mecanism
