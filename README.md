# Phantom GUI

[Phantom](https://github.com/jhead/phantom) is a command line application to make Bedrock servers show up as LAN servers for consoles, but it doesn't have a GUI.

I have non-tech savvy friends that want to play on my Bedrock server and only have it on console, so I made this to try and alleviate some of the pain. It uses Python 3 with pywebview, using Python to orchestrate starting/stopping Phantom and HTML/CSS for the GUI.

## Preparing the GUI

### Downloading the GUI and Dependencies

There are two required items you have to download:

- [phantom CLI](https://github.com/jhead/phantom/releases)
- One of the following:
  - [Phantom GUI](https://github.com/BenShoeman/phantom-gui/releases) if running the app/exe (Windows 32/64-bit and macOS x86_64 only)
  - A clone of this repo if running manually

You can clone this repo and run `main.py` manually. There is one dependency you need which you can install through pip:

```sh
pip3 install pywebview
```

After that, you can run `main.py` through python3.

### Adding the Phantom CLI

There is one step that needs to happen before running the GUI. The phantom CLI executable for your platform, titled something like `phantom-<os>`, **needs to be placed in the `bin` folder.**

This should be straightforward for the Windows release or if you run it manually from the `.py` file, as the `bin` folder is in the root. Just place the `phantom-<os>` executable in that folder. If you're on GNU/Linux you will likely need to run `chmod +x phantom-linux` on the executable too.

You will need to create a firewall rule for this to work. Windows should automatically prompt you to allow outside connections.

If you're on macOS, there are some steps you need to follow to get it to run:

1. Control-click the folder you saved the `phantom-macos` executable to and click *New Terminal at Folder*.
2. Run the following command in the terminal: `chmod +x phantom-macos`
3. Control-click the `phantom-macos` file and click *Open*. Then click *Open* again. It will open a terminal window, you can just close out of it.
4. Control-click `Phantom-GUI.app` and click *Show Package Contents*.
5. Navigate to Contents &rarr; Resources &rarr; bin
6. Place the `phantom-macos` executable here.
7. Finally, control-click `Phantom-GUI.app` and click *Open*, then click *Open* again. (If Apple tries to strong-arm you into moving it into Trash, just click *Cancel* and do this step again... it should then let you click *Open*.)

These steps are only necessary because Apple likes to make it as difficult as possible to run apps that weren't downloaded from the App Store. -___- After this, you should be able to open it like any other application.

If the LAN server does not show up, you will also have to allow `Phantom-GUI.app` connections through the firewall in System Preferences and then close and re-open Phantom-GUI.

## Using the GUI

The GUI is designed to be as simple as possible, so it should be straightforward. It looks like so:

![The GUI upon first start](/doc/gui.png?raw=true)

Input the server URL and port number in the fields and then click *Start Phantom Proxy*, and you should be good to go. If something went wrong, it will pop up an error message explaining what to do to resolve the issue.

The GUI will remember what URL/port you connected to last upon re-opening the application.

## Building the GUI

Make sure to install the `pywebview` dependency before building.

### py2app (macOS)

First install py2app through pip3 if you don't have it, then `cd` into the `make` folder and run the following command:

```sh
python3 setup-py2app.py py2app
```

### pyinstaller (other platforms)

Untested outside of Windows but theoretically should work on other platforms.

First install pyinstaller through pip if you don't have it, then `cd` into the `make` folder and run the following command:

```sh
pyinstaller setup-pyinstaller.spec
```

## Working Platforms

The GUI definitely works on the following OSs:

- Windows 10, 32-bit and 64-bit
- macOS Big Sur, x86_64

I see no issues running it on the following as well, bare minimum by running it manually:

- Windows 8, 8.1, 32-bit and 64-bit
- macOS Catalina
- Most GNU/Linux distros, x86_64 and ARM

Phantom CLI works with Minecraft Bedrock Edition on Windows 10, iOS, Android, Xbox One, and PS4 (**NOT** Switch, as it doesn't support LAN games!).