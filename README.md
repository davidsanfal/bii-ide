#bii-IDE

**Bii-IDE** is an **ide for Arduino** that integrates all the functionality of [biicode](http://biicode.com/). You can [download the biiGUI package](https://www.biicode.com/downloads) from the biicode download site.

With [biicode](http://biicode.com/) you can:

1. **Save your project in different folders** for a better organization.

2. **Reuse yours and other users'code.** Reusing made easy: just `#include` the file you need and you get it. No more copy and paste files from project to project or dowloading zip files from tutorials.

3. This is a **simple** and **fast** way to **compile and upload** your code in your Arduino.

5. biicode are hosting adafruit, sparkfun and many other libraries, **you won’t need to download and install libraries in your SDK anymore**.

##User guide

###1. Select your workspace or create one

![](https://github.com/davidsanfal/bii-ide/blob/master/docs/images/create_ws.png)

![](https://github.com/davidsanfal/bii-ide/tree/master/docs/images/select_ws.png)

![](https://github.com/davidsanfal/bii-ide/tree/master/docs/images/selected_ws.png)

###2. Check out the interface

![](https://github.com/davidsanfal/bii-ide/tree/master/docs/images/ide.png)

![](https://github.com/davidsanfal/bii-ide/tree/master/docs/images/ide_file.png)

####2.1 Menu and Tools bar

####2.2 Workspace info

####2.3 Edition site

####2.4 Biicode commands

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

    git clone git://github.com/biicode/bii-ide.git
    cd bii-ide/bii-ide
    python bii_ide.py
