# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'serval_dialog_base.ui'
#
# Created: Thu Dec 31 14:34:28 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Serval(object):
    def setupUi(self, Serval):
        Serval.setObjectName(_fromUtf8("Serval"))
        Serval.resize(659, 42)
        self.gridLayout_2 = QtGui.QGridLayout(Serval)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(Serval)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.rastersCbo = QtGui.QComboBox(Serval)
        self.rastersCbo.setMinimumSize(QtCore.QSize(200, 0))
        self.rastersCbo.setObjectName(_fromUtf8("rastersCbo"))
        self.horizontalLayout.addWidget(self.rastersCbo)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(Serval)
        QtCore.QMetaObject.connectSlotsByName(Serval)

    def retranslateUi(self, Serval):
        Serval.setWindowTitle(_translate("Serval", "Serval", None))
        self.label.setText(_translate("Serval", "Raster", None))

