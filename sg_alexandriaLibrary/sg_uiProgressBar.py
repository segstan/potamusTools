# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:/Data/Scripts/maya/python/envLibrary/ui/ui_sgEnvProgressBar.ui'
#
# Created: Mon Jun  8 21:36:17 2020
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_windowSGProgressBarLibrary(object):
    def setupUi(self, windowSGProgressBarLibrary):
        windowSGProgressBarLibrary.setObjectName("windowSGProgressBarLibrary")
        windowSGProgressBarLibrary.resize(300, 100)
        windowSGProgressBarLibrary.setMinimumSize(QtCore.QSize(300, 100))
        windowSGProgressBarLibrary.setMaximumSize(QtCore.QSize(300, 100))
        self.progressBar_sgLoadEnvWin = QtWidgets.QProgressBar(windowSGProgressBarLibrary)
        self.progressBar_sgLoadEnvWin.setGeometry(QtCore.QRect(10, 40, 281, 23))
        self.progressBar_sgLoadEnvWin.setProperty("value", 0)
        self.progressBar_sgLoadEnvWin.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.progressBar_sgLoadEnvWin.setTextVisible(True)
        self.progressBar_sgLoadEnvWin.setInvertedAppearance(False)
        self.progressBar_sgLoadEnvWin.setObjectName("progressBar_sgLoadEnvWin")
        self.label_sgProgressBarWin = QtWidgets.QLabel(windowSGProgressBarLibrary)
        self.label_sgProgressBarWin.setGeometry(QtCore.QRect(10, 10, 281, 20))
        self.label_sgProgressBarWin.setText("")
        self.label_sgProgressBarWin.setAlignment(QtCore.Qt.AlignCenter)
        self.label_sgProgressBarWin.setObjectName("label_sgProgressBarWin")

        self.retranslateUi(windowSGProgressBarLibrary)
        QtCore.QMetaObject.connectSlotsByName(windowSGProgressBarLibrary)

    def retranslateUi(self, windowSGProgressBarLibrary):
        windowSGProgressBarLibrary.setWindowTitle(QtWidgets.QApplication.translate("windowSGProgressBarLibrary", "Loading Env Library UI", None, -1))

