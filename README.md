# potamusTools

To Install the Alexandria library from maya, houdini or nuke with python 3.x:
```
import sys
sys.path.append("D:/Scripts/potamusTools/sg_alexandriaLibrary")

import sg_alexandriaInstall
import imp
imp.reload(sg_alexandriaLibrary)

sg_alexandriaLibrary.sg_alexandriaLibrary_UI()
```

Then follow the instructions.
