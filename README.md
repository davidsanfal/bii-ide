#biiGUI

**BiiGUI** is an **ide for Arduino** that integrates all the functionality of [biicode](http://biicode.com/). You can [download the biiGUI package](https://www.biicode.com/downloads) from the biicode download site.

With [biicode](http://biicode.com/) you can:

1. **Save your project in different folders** for a better organization.

2. **Reuse yours and other users'code.** Reusing made easy: just `#include` the file you need and you get it. No more copy and paste files from project to project or dowloading zip files from tutorials.

3. This is a **simple** and **fast** way to **compile and upload** your code in your Arduino.

5. biicode are hosting adafruit, sparkfun and many other libraries, **you won’t need to download and install libraries in your SDK anymore**.

##User guide

###1. Select your workspace or create one

###2. Check out the interface

####2.1 Menu bar

1. File
2. Workspace
3. commands
4. About

####2.2 Toolbars

####2.3 Workspace info

1. Projects
2. Bloks
3. File treeview

####2.4 Edition site

1. Text editor
	1. Text editor
	2. Arduino docs
2. Terminal

####2.5 Biicode commands

1. [settings](http://docs.biicode.com/arduino/reference/commands.html#bii-arduino-settings-managing-your-hive-settings)
2. [find](http://docs.biicode.com/biicode/reference/commands.html#bii-find-retrieving-dependencies)
3. [build](http://docs.biicode.com/arduino/reference/commands.html#bii-arduino-build-build-the-project)
4. [upload](http://docs.biicode.com/arduino/reference/commands.html#bii-arduino-upload-upload-a-firmware-in-arduino)
5. monitor
6. terminal

##Code dependencies

-   [biicode](https://www.biicode.com/downloads)
-   [Python 2.7](http://www.python.org/)
-   [PyQt4](http://www.riverbankcomputing.com/software/pyqt/intro)

##Cloning and Running

    git clone git://github.com/[USER]/biigui.git
    cd biigui/biigui
    python biigui.py

##License

-   GPL v3
