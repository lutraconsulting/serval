# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'serval_dialog_base.ui'
#
# Created: Sat Jan 02 16:39:00 2016
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import resources

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
        Serval.resize(200, 80)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Serval.sizePolicy().hasHeightForWidth())
        Serval.setSizePolicy(sizePolicy)
        Serval.setMinimumSize(QtCore.QSize(200, 80))
        Serval.setMaximumSize(QtCore.QSize(400, 100))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/icons/serval_icon.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Serval.setWindowIcon(icon)
        self.gridLayout_2 = QtGui.QGridLayout(Serval)
        self.gridLayout_2.setMargin(3)
        self.gridLayout_2.setSpacing(3)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setContentsMargins(-1, 0, -1, 0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.refreshRastersBtn = QtGui.QToolButton(Serval)
        self.refreshRastersBtn.setAccessibleDescription(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/icons/refreshRasters.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.refreshRastersBtn.setIcon(icon1)
        self.refreshRastersBtn.setIconSize(QtCore.QSize(24, 24))
        self.refreshRastersBtn.setObjectName(_fromUtf8("refreshRastersBtn"))
        self.horizontalLayout.addWidget(self.refreshRastersBtn)
        self.rastersCbo = QtGui.QComboBox(Serval)
        self.rastersCbo.setMinimumSize(QtCore.QSize(150, 0))
        self.rastersCbo.setObjectName(_fromUtf8("rastersCbo"))
        self.horizontalLayout.addWidget(self.rastersCbo)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(Serval)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.valueEdit = QtGui.QLineEdit(Serval)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.valueEdit.sizePolicy().hasHeightForWidth())
        self.valueEdit.setSizePolicy(sizePolicy)
        self.valueEdit.setMinimumSize(QtCore.QSize(80, 0))
        self.valueEdit.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.valueEdit.setObjectName(_fromUtf8("valueEdit"))
        self.horizontalLayout_2.addWidget(self.valueEdit)
        self.changeCellValueBtn = QtGui.QToolButton(Serval)
        self.changeCellValueBtn.setAccessibleDescription(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/icons/setValue.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.changeCellValueBtn.setIcon(icon2)
        self.changeCellValueBtn.setIconSize(QtCore.QSize(24, 24))
        self.changeCellValueBtn.setObjectName(_fromUtf8("changeCellValueBtn"))
        self.horizontalLayout_2.addWidget(self.changeCellValueBtn)
        self.webpageBtn = QtGui.QToolButton(Serval)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/icons/helpContents.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.webpageBtn.setIcon(icon3)
        self.webpageBtn.setIconSize(QtCore.QSize(24, 24))
        self.webpageBtn.setObjectName(_fromUtf8("webpageBtn"))
        self.horizontalLayout_2.addWidget(self.webpageBtn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 1, 0, 1, 1)

        self.retranslateUi(Serval)
        QtCore.QMetaObject.connectSlotsByName(Serval)

    def retranslateUi(self, Serval):
        Serval.setWindowTitle(_translate("Serval", "Serval", None))
        self.refreshRastersBtn.setToolTip(_translate("Serval", "Refresh Rasters List", None))
        self.refreshRastersBtn.setWhatsThis(_translate("Serval", "Use after loading a new raster into canvas", None))
        self.refreshRastersBtn.setText(_translate("Serval", "Refresh Rasters List", None))
        self.rastersCbo.setToolTip(_translate("Serval", "Editable Rasters List", None))
        self.label_2.setText(_translate("Serval", "Value", None))
        self.valueEdit.setToolTip(_translate("Serval", "Enter a new cell value and press Enter", None))
        self.valueEdit.setWhatsThis(_translate("Serval", "Enter a new cell value and press Enter. It is immediately written to disk.", None))
        self.changeCellValueBtn.setToolTip(_translate("Serval", "Save the new cell raster value to disk", None))
        self.changeCellValueBtn.setWhatsThis(_translate("Serval", "Save the new value to disk", None))
        self.changeCellValueBtn.setText(_translate("Serval", "...", None))
        self.webpageBtn.setToolTip(_translate("Serval", "Open plugin\'s webpage (GitHub wiki)", None))
        self.webpageBtn.setWhatsThis(_translate("Serval", "Open plugin\'s webpage.", None))
        self.webpageBtn.setText(_translate("Serval", "...", None))