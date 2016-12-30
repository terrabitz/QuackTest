# QuackTest

This is just a simple script to test duckyscripts before putting
them onto the ducky itself. It can often take a while to write the 
script, encode it, mount the SD card, transfer the encoded script,
and test it with the ducky. So this little interpreter is designed to 
allow slightly faster development of the scripts by emulating a 
rubber ducky.

## Prerequisites

### Linux

You need a few prequisite packages before attempting to install the
package. These include Python3, the XLib library, and the Python
Tkinter library. On Linux these can be installed using your package
manager, as with the following command:

```
sudo apt install python3 python3-xlib python3-tk
```

### Windows

On Windows, you just need to have a correct version of python available
on the system. This has been tested using Python 3.5. Please note, if
you want to use the build scripts, you must install `pyinstaller`
separately (as this seems to have some troubles on the latest 3.5 and
3.6 Python using Pip). Using Python version 3.5.0 seems to work.

## Installation

To install QuackTest on the target computer, just run the included
`setup.py` script using the command
```
python3 setup.py install
```
This also will install the `quacktest.py` and `quacktest-gui.py` scripts
onto your system.

## Building

Optionally, you can also use build or use binaries precompiled for
your target environment. This is especially useful if you want to deploy
QuackTest onto a fresh environment, without needing to install all
its dependencies. You can make these using the included `build_dist.py`
script and will utilize the `pyinstaller` package (which must be
installed on your system). The binaries will be placed under the `dist`
directory under the appropriate system name, and will consist of the
"one file" build and "one directory" build for both the command line
and GUI builds. Please note, this build
script has only been tested on Windows 7 and Ubuntu 16.04, and (as per
pyinstaller) must be ran on the target system being compiled for.

Also, for `pyinstaller`, the "one file" output tends to behave oddly on
unpatched Windows 7 systems. If this is your target environment, please
use the output of the "one directory" output, as this seems to work.

## Usage

To use the script, you can use either the command line utility or the
GUI. Both are included in the `bin` directory, and can be invoked by
using `quacktest.py` or `quacktest-gui.py`, respectively.