#!/bin/bash

rm ~/.local/share/okular/docdata/*.20yearsofKDE.pdf.xml
rm ~/.config/okular*
sed -i '/^lastVisited/d' ~/.config/QtProject.conf

cd ../usage_scenarios/test_data

okular &
sleep 1

WID=`xdotool getactivewindow`
xdotool windowsize $WID 1200 800
xdotool windowmove --sync $WID 0 0

xdotool key ctrl+o
sleep 1
xdotool type "20yearsofKDE.pdf"
sleep 1
xdotool key Return
sleep 1

xdotool key ctrl+g
sleep 1
xdotool type "97"
sleep 1
xdotool key Return
sleep 1

xdotool key Next
sleep 1

xdotool key F6
sleep 1
xdotool key 1
sleep 1
xdotool mousemove 419 172
xdotool click 1
sleep 1
xdotool type "This is an important bit of history"
xdotool key Return
sleep 1

xdotool key alt+v
sleep 1
xdotool key Down Down Down Down Down Down Down Down
xdotool key Right Down
sleep 1
xdotool key Return
sleep 1

xdotool key ctrl+0
sleep 1
xdotool key ctrl++
sleep 1
xdotool key ctrl++
sleep 1
xdotool key ctrl++
sleep 1

xdotool key ctrl+0
sleep 1
xdotool key ctrl+minus
sleep 1
xdotool key ctrl+minus
sleep 1

xdotool key ctrl+shift+p
sleep 1
xdotool key Escape
sleep 1

xdotool key Left
sleep 1
xdotool key Left
sleep 1
xdotool key Left
sleep 1
xdotool key Left
sleep 1

xdotool key Escape
sleep 1

xdotool key ctrl+shift+comma
sleep 1
xdotool key Down
sleep 1
xdotool key Tab Tab Tab Tab Tab
sleep 1
xdotool key space
sleep 1
xdotool key alt+k
sleep 1

xdotool key alt+v
sleep 1
xdotool key Down Down Down Down Down Down Down Down Down
xdotool key Right
sleep 1
xdotool key Return
sleep 1

xdotool key ctrl+0
sleep 1
xdotool key ctrl+minus
sleep 1

xdotool key ctrl+g
sleep 1
xdotool type "111"
sleep 1
xdotool key Return
sleep 1

xdotool key ctrl+4
sleep 1
xdotool mousemove 483 320
xdotool mousedown 1
sleep 1
xdotool mousemove 567 360
sleep 1
xdotool mouseup 1
sleep 1

xdotool key ctrl+shift+p
sleep 1
xdotool key Escape
sleep 1

xdotool key Right
sleep 1
xdotool key Right
sleep 1
xdotool key Right
sleep 1
xdotool key Right
sleep 1
xdotool key Right
sleep 1
xdotool key Right
sleep 1
xdotool key Right
sleep 1
xdotool key Right
sleep 1
xdotool key Right
sleep 1
xdotool key Right
sleep 1
xdotool key Right
sleep 1
xdotool key Right
sleep 1
xdotool key Right
sleep 1
xdotool key Right
sleep 1

xdotool key Escape
sleep 1

xdotool key ctrl+q
xdotool key Right Return
