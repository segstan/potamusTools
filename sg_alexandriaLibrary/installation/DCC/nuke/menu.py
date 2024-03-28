import nuke
import importlib
import sg_alexandriaLibrary
importlib.reload(sg_alexandriaLibrary)

## Add Alexandria Toolbar
toolbar= nuke.menu('Nuke')
libraryMenu = toolbar.addMenu('Library')
libraryMenu.addCommand(name = 'Alexandria Library',command = 'importlib.reload(sg_alexandriaLibrary);sg_alexandriaLibrary.sg_alexandriaLibrary_UI()',shortcut = "CTRL+Shift+L")

