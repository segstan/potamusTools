"""
NAME: Library
ICON: D:/Scripts/common/sg_alexandriaLibrary/icons/sg_alexandriaLibrary_icon64.png
KEYBOARD_SHORTCUT: Ctrl+Shift+L
SCOPE:
Alexandria Library

"""

# The following symbols are added when run as a shelf item script:
# exit():      Allows 'error-free' early exit from the script.
# console_print(message, raiseTab=False):
#              Prints the given message to the result area of the largest
#              available Python tab.
#              If raiseTab is passed as True, the tab will be raised to the
#              front in its pane.
#              If no Python tab exists, prints the message to the shell.
# console_clear(raiseTab=False):
#              Clears the result area of the largest available Python tab.
#              If raiseTab is passed as True, the tab will be raised to the
#              front in its pane.

import sys
sys.path.append("D:/Scripts/common/sg_alexandriaLibrary")
#sys.path.append("D:/Scripts/common/sg_pergamonLibrary/Tabs")

import sg_alexandriaLibrary
import imp
imp.reload(sg_alexandriaLibrary)

sg_alexandriaLibrary.sg_alexandriaLibrary_UI()


