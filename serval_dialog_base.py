# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'serval_dialog_base.ui'
#
# Created: Thu Feb 25 22:33:56 2016
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
        Serval.resize(201, 90)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Serval.sizePolicy().hasHeightForWidth())
        Serval.setSizePolicy(sizePolicy)
        Serval.setMinimumSize(QtCore.QSize(160, 90))
        Serval.setMaximumSize(QtCore.QSize(400, 110))
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
        self.curRasterLabel = QtGui.QLabel(Serval)
        self.curRasterLabel.setObjectName(_fromUtf8("curRasterLabel"))
        self.verticalLayout_2.addWidget(self.curRasterLabel)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.mColorButton = QgsColorButtonV2(Serval)
        self.mColorButton.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.mColorButton.setObjectName(_fromUtf8("mColorButton"))
        self.horizontalLayout.addWidget(self.mColorButton)
        self.probeBtn = QtGui.QToolButton(Serval)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/icons/mIconColorPicker.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probeBtn.setIcon(icon1)
        self.probeBtn.setIconSize(QtCore.QSize(24, 24))
        self.probeBtn.setObjectName(_fromUtf8("probeBtn"))
        self.horizontalLayout.addWidget(self.probeBtn)
        self.pencilBtn = QtGui.QToolButton(Serval)
        self.pencilBtn.setAccessibleDescription(_fromUtf8(""))
        self.pencilBtn.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/icons/mActionToggleEditing.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pencilBtn.setIcon(icon2)
        self.pencilBtn.setIconSize(QtCore.QSize(24, 24))
        self.pencilBtn.setCheckable(False)
        self.pencilBtn.setObjectName(_fromUtf8("pencilBtn"))
        self.horizontalLayout.addWidget(self.pencilBtn)
        self.webpageBtn = QtGui.QToolButton(Serval)
        self.webpageBtn.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/icons/helpContents.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.webpageBtn.setIcon(icon3)
        self.webpageBtn.setIconSize(QtCore.QSize(24, 24))
        self.webpageBtn.setObjectName(_fromUtf8("webpageBtn"))
        self.horizontalLayout.addWidget(self.webpageBtn)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.bandSpinBoxesLayout = QtGui.QHBoxLayout()
        self.bandSpinBoxesLayout.setObjectName(_fromUtf8("bandSpinBoxesLayout"))
        self.verticalLayout_2.addLayout(self.bandSpinBoxesLayout)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 1, 0, 1, 1)

        self.retranslateUi(Serval)
        QtCore.QMetaObject.connectSlotsByName(Serval)

    def retranslateUi(self, Serval):
        Serval.setWindowTitle(_translate("Serval", "Serval", None))
        self.curRasterLabel.setText(_translate("Serval", "R:", None))
        self.mColorButton.setToolTip(_translate("Serval", "Color Button", None))
        self.mColorButton.setStatusTip(_translate("Serval", "Color Button", None))
        self.mColorButton.setWhatsThis(_translate("Serval", "Color Button", None))
        self.mColorButton.setAccessibleName(_translate("Serval", "Color Button", None))
        self.mColorButton.setText(_translate("Serval", "Color picker", None))
        self.probeBtn.setText(_translate("Serval", "...", None))
        self.pencilBtn.setToolTip(_translate("Serval", "Turns on/off the Locked Mode", None))
        self.pencilBtn.setStatusTip(_translate("Serval", "Turns on/off the Locked Mode", None))
        self.pencilBtn.setWhatsThis(_translate("Serval", "Turns on/off the Locked Mode", None))
        self.pencilBtn.setText(_translate("Serval", "...", None))
        self.webpageBtn.setToolTip(_translate("Serval", "Open plugin\'s webpage (GitHub wiki)", None))
        self.webpageBtn.setStatusTip(_translate("Serval", "Open plugin\'s webpage (GitHub wiki)", None))
        self.webpageBtn.setWhatsThis(_translate("Serval", "Open plugin\'s webpage (GitHub wiki)", None))
        self.webpageBtn.setText(_translate("Serval", "...", None))

from qgscolorbuttonv2 import QgsColorButtonV2
import resources_rc
