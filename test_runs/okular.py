#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2020 Cornelius Schumacher <schumacher@kde.org>

from pathlib import Path

class XDoWriter:
    def __init__(self):
        self.script = ""

    def write_script(self):
        path = Path(__file__).resolve().parent / "okular.sh"
        with path.open("w") as f:
            f.write(self.script)

    def add(self, line=""):
        self.script += line + "\n"

    def xdo(self, args):
        self.add("xdotool " + args)

    def key(self, symbol, repeat=1):
        self.xdo("key" + (" " + symbol) * repeat)

    def key_ctrl(self, symbol):
        self.key("ctrl+" + symbol)

    def keys(self, string):
        self.xdo(f'type "{string}"')

    def mousemove(self, point):
        self.xdo(f"mousemove {point[0]} {point[1]}")

    def click(self):
        self.xdo("click 1")

    def sleep(self, seconds=1):
        self.add(f"sleep {seconds}")

    def she_bang(self):
        self.add("#!/bin/bash")
        self.add()

    def clear_files(self, filename):
        self.add("rm " + filename)

    def clear_line_of_file(self, filename, pattern):
        self.add(f"sed -i '/{pattern}/d' {filename}")

    def cd(self, wd):
        self.add(f"cd {wd}")
        self.add()

    def start_application(self, name):
        self.add(name + " &")
        self.sleep()
        self.add()

    def reset_window(self):
        self.add("WID=`xdotool getactivewindow`")
        self.xdo("windowsize $WID 1200 800")
        self.xdo("windowmove --sync $WID 0 0")
        self.add()

    def quit_application(self, discard=False):
        self.key_ctrl("q")
        if discard:
            self.key("Right Return")
        else:
            self.key("Escape")


class OkularWriter(XDoWriter):
    def __init__(self):
        super().__init__()

    def open_file(self, name):
        self.key_ctrl("o")
        self.sleep()
        self.keys("20yearsofKDE.pdf")
        self.sleep()
        self.key("Return")
        self.sleep()
        self.add()

    def goto_page(self, number):
        self.key_ctrl("g")
        self.sleep()
        self.keys(str(number))
        self.sleep()
        self.key("Return")
        self.sleep()
        self.add()

    def page_down(self):
        self.key("Next")
        self.sleep()
        self.add()

    def add_note(self):
        self.key("F6")
        self.sleep()
        self.key("1")
        self.sleep()
        self.mousemove((419, 172))
        self.click()
        self.sleep()
        self.keys("This is an important bit of history")
        self.key("Return")
        self.sleep()
        self.add()

    def rotate_right(self):
        self.key("alt+v")
        self.sleep()
        self.key("Down", 8)
        self.key("Right Down")
        self.sleep(1)
        self.key("Return")
        self.sleep(1)
        self.add()

    def rotate_left(self):
        self.key("alt+v")
        self.sleep()
        self.key("Down", 9)
        self.key("Right")
        self.sleep(1)
        self.key("Return")
        self.sleep(1)
        self.add()

    def zoom_in(self, factor):
        self.key_ctrl("0")
        self.sleep()
        for i in range(0, factor):
            self.key_ctrl("+")
            self.sleep()
        self.add()

    def zoom_out(self, factor):
        self.key_ctrl("0")
        self.sleep()
        for i in range(0, factor):
            self.key_ctrl("minus")
            self.sleep()
        self.add()

    def start_presentation(self):
        self.key("ctrl+shift+p")
        self.sleep()
        self.key("Escape")
        self.sleep()
        self.add()

    def exit_presentation(self):
        self.key("Escape")
        self.sleep()
        self.add()

    def page_back(self, count):
        for i in range(0, count):
            self.key("Left")
            self.sleep()
        self.add()

    def page_forward(self, count):
        for i in range(0, count):
            self.key("Right")
            self.sleep()
        self.add()

    def activate_inverted_colors(self):
        self.key("ctrl+shift+comma")
        self.sleep()
        self.key("Down")
        self.sleep()
        self.key("Tab", 5)
        self.sleep()
        self.key("space")
        self.sleep()
        self.key("alt+k")
        self.sleep()
        self.add()

    def select_text(self):
        self.key_ctrl("4")
        self.sleep()
        self.mousemove((483, 320))
        self.xdo("mousedown 1")
        self.sleep()
        self.mousemove((567, 360))
        self.sleep()
        self.xdo("mouseup 1")
        self.sleep()
        self.add()

    def run(self):
        self.she_bang()

        self.clear_files("~/.local/share/okular/docdata/*.20yearsofKDE.pdf.xml")
        self.clear_files("~/.config/okular*")
        self.clear_line_of_file("~/.config/QtProject.conf", "^lastVisited")
        self.add()

        self.cd("../usage_scenarios/test_data")

        self.start_application("okular")

        self.reset_window()

        self.open_file("20yearsofKDE.pdf")
        self.goto_page(97)
        self.page_down()
        self.add_note()
        self.rotate_right()
        self.zoom_in(3)
        self.zoom_out(2)
        self.start_presentation()
        self.page_back(4)
        self.exit_presentation()
        self.activate_inverted_colors()
        self.rotate_left()
        self.zoom_out(1)
        self.goto_page(111)
        self.select_text()
        self.start_presentation()
        self.page_forward(14)
        self.exit_presentation()

        self.quit_application(discard=True)

        self.write_script()

OkularWriter().run()
