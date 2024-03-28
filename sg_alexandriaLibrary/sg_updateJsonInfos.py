import os
import sys
import glob
import json
import time
from datetime import datetime,timedelta

pythonVersion = (sys.version_info[0])

import sg_functions as fcn
if pythonVersion == 2:
    reload(fcn)
elif pythonVersion == 3:
    import imp
    imp.reload(fcn)

# if in_katana == True :
# 	from PyQt5 import QtWidgets,QtGui, QtCore, QtWidgets , uic 
# 	from PyQt5.QtGui import QMovie
# else:
from PySide2 import QtGui, QtCore, QtWidgets , QtUiTools
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QObject
from PySide2.QtCore import QEvent
from PySide2.QtGui import QMovie

class sgUpdateJsonInfos(QtWidgets.QMainWindow):
    def __init__(self, parent = QtWidgets.QApplication.activeWindow()):
        super(sgUpdateJsonInfos, self).__init__(parent)
        # Load in your UI file.
        self.platform = sys.platform
        fileDir = os.path.dirname(os.path.abspath(__file__))
        file_interface = os.path.abspath(fileDir+ "/ui/ui_sgUpdateInfosLib.ui")

        self.loader = QUiLoader()
        self.mainUI = self.loader.load(file_interface,self)
        self.mainUI.pb_updateAllJsonInfos.clicked.connect(self.updateJsonInfosLibrary)

        self.setWindowTitle("Update Json Infos for Library 2.x.x")

    def appendUI(self,path):
        self.mainUI.lineEdit_sgNameEntry.setText(path)

    def parseLibrary(self,pathLibrary):
        listJson = []
        for root,dirs,files in os.walk(pathLibrary):
            for file in files:
                if file.endswith("_infos.json"):
                    #print(os.path.join(root,file))
                    listJson.append(os.path.join(root,file))
        return listJson

    def updateDictInfos(self,jsonInfosFile,listUpdatedFiles):
        try:
            dictInfos = fcn.readJsonfile(jsonInfosFile)
        except:
            print("ERROR: ", jsonInfosFile)
            print(sys.exc_info())
            return False

        dataKeys = len(dictInfos["releaseInfos"][0].keys())

        if dataKeys < 11:
            listUpdatedFiles.append(jsonInfosFile)
            for key in dictInfos["releaseInfos"][0]:
                # Get Old Data
                if key == "author":
                    author = dictInfos["releaseInfos"][0]["author"]
                elif key == "available":
                    listExtensionAvailable =  dictInfos["releaseInfos"][0]["available"]
                elif key == "name":
                    name = dictInfos["releaseInfos"][0]["name"]
                elif key == "tags":
                    tags = dictInfos["releaseInfos"][0]["tags"]
                elif key == "note":
                    note = dictInfos["releaseInfos"][0]["note"]
                elif key == "version":
                    version = dictInfos["releaseInfos"][0]["version"]
                elif key == "meta":
                    meta = dictInfos["releaseInfos"][0]["meta"]
                elif key == "timeEntry":
                    timeEntry = dictInfos["releaseInfos"][0]["timeEntry"]
                elif key == "lock":
                    lock = dictInfos["releaseInfos"][0]["lock"]
                elif key == "ocio":
                    ocio = dictInfos["releaseInfos"][0]["ocio"]
                elif key == "textures":
                    listTextures = dictInfos["releaseInfos"][0]["textures"]

            # Check Variables has been set
            if 'listTextures' not in locals():
                listTextures = []
            if 'ocio' not in locals():
                ocio = ""
            if 'lock' not in locals():
                lock = False
            if 'timeEntry' not in locals():
                timeEntry = time.time()
            if 'listExtensionAvailable' not in locals():
                listExtensionAvailable = []
            if 'meta' not in locals():
                meta = ""

            # Set
            dictUpdatedInfos = fcn.createDictJsonEntryInfos(name,listExtensionAvailable,listTextures,note,version,tags,ocio,timeEntry,meta)
            try:
                print(json.dumps(dictUpdatedInfos,indent = 4))
            except:
                print(dictUpdatedInfos)
                print(sys.exc_info())
                return False

            # Save
            fcn.writeJsonFile(jsonInfosFile,dictUpdatedInfos)
        
        return listUpdatedFiles

    def updateJsonInfosLibrary(self):
        pathLibrary = "E:/Data/library"
        listJson = self.parseLibrary(pathLibrary)
        listUpdatedFiles = []
        for file in listJson:
            listUpdatedFiles = self.updateDictInfos(file,listUpdatedFiles)

        if listUpdatedFiles:
            print("Total File Updated: " + str(len(listUpdatedFiles)))
            print("File Infos Json updated: " + str(len(listUpdatedFiles)) +"\n" + '\n'.join("- " + str(p) for p in sorted(listUpdatedFiles)))



# def sgUpdateJsonInfos_UI():
#     ## Delete all previous instances
#     for entry in QtWidgets.QApplication.allWidgets():
#         if type(entry).__name__ == 'sgUpdateJsonInfos':
#             entry.close()
#             entry.deleteLater()

#     ui = sgUpdateJsonInfos()
#     ui.show()