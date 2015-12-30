# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import re
from os.path import dirname, join, isfile, getsize
import numpy as np



def is_number(s):
    try:
        if np.isnan(float(s)):
            raise ValueError
        float(s)
        return True
    except ValueError:
        return False


class QCustomTableWidgetItem (QTableWidgetItem):
  def __lt__(self, other):
    try:
      return ( float(self.text()) <
            float(other.text()) )
    except:
      return QTableWidgetItem.__lt__(self, other)


class CustomTable(QTableWidget):
    def __init__(self, parent = None):
        QTableWidget.__init__(self, parent)
        if parent:
            self.parent = parent
        # self.refModel = self.parent.refModel
        self.__initActions__()
        self.__initContextMenus__()
        self.horizontalHeader().setVisible(True)
        self.workDists = []
        self.workVals = []
        self.workValsForRef = []
        self.refDists = []
        self.refVals = []
        self.corr = []

    def __initContextMenus__(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.connect(self, SIGNAL("customContextMenuRequested(QPoint)"), self.tableWidgetContext)
        self.setSortingEnabled(True)

    def tableWidgetContext(self, point):
        '''Create a menu for the tableWidget and associated actions'''
        tw_menu = QMenu("Menu", self)
        tw_menu.addAction(self.pasteAction)
        tw_menu.addAction(self.countAction)
        tw_menu.addAction(self.copyAction)
        tw_menu.addAction(self.insRowAction)
        tw_menu.addAction(self.insColAction)
        tw_menu.exec_(self.mapToGlobal(point))

    def addData(self, data, startrow=None,  startcol = None):
        if startcol:
            sc = startcol #start column
        else:
            sc = 0 # n is for columns
        if startrow:
            sr = startrow
        else:
            sr = 0
        m = sr
        for row in data:
            n = sc
            for item in row:
                newitem = QTableWidgetItem(item)
                self.setItem(m,  n,  newitem)
                n+=1
            m+=1

    def __initActions__(self):
        self.pasteAction = QAction("Paste",  self)
        self.pasteAction.setShortcut("Ctrl+V")
        self.addAction(self.pasteAction)
        self.connect(self.pasteAction, SIGNAL("triggered()"), self.pasteMike11)
        self.copyAction = QAction("Copy",  self)
        self.copyAction.setShortcut("Ctrl+C")
        self.addAction(self.copyAction)
        self.connect(self.copyAction, SIGNAL("triggered()"), self.copyCells)
        self.insColAction = QAction("Insert Column",  self)
        self.addAction(self.insColAction)
        self.connect(self.insColAction, SIGNAL("triggered()"), self.addColumns)
        self.insRowAction = QAction("Insert Row",  self)
        self.addAction(self.insRowAction)
        self.connect(self.insRowAction, SIGNAL("triggered()"), self.addRows)

    def addRows(self):
        selRange  = self.selectedRanges()[0]
        topRow = selRange.topRow()
        bottomRow = selRange.bottomRow()
        for i in xrange(topRow, (bottomRow+1)):
            self.insRow(i)

    def addColumns(self):
        selRange  = self.selectedRanges()[0]
        rightColumn = selRange.rightColumn()
        leftColumn = selRange.leftColumn()
        for i in xrange(leftColumn, (rightColumn+1)):
            self.insCol(i)

    def insCol(self,  col = None):
        if type(col) is int:
            self.insertColumn(col)
        else:
            self.insertColumn(self.currentColumn())

    def insRow(self,  row = None):
        if type(row) is int:
            self.insertRow(row)
        else:
            self.insertRow(self.currentRow())

    def pasteClip(self):
        cb = QApplication.clipboard()
        clipText = cb.text()
        clip2paste = self.splitClipboard(clipText)
        selRange  = self.selectedRanges()[0]
        topRow = selRange.topRow()
        bottomRow = selRange.bottomRow()
        rightColumn = selRange.rightColumn()
        leftColumn = selRange.leftColumn()
        if (len(clip2paste)+topRow) >= self.rowCount():
            self.setRowCount(len(clip2paste)+topRow)
        if (len(clip2paste[0])+rightColumn) >= self.columnCount():
            self.setColumnCount(len(clip2paste[0])+rightColumn)
        self.addData(clip2paste, topRow,  leftColumn)
        self.calcDiff()
        self.setColors()

    def pasteMike11(self):
        cb = QApplication.clipboard()
        clipText = cb.text()
        clip2paste = self.splitClipboard(clipText)
        if len(clip2paste)-1 >= self.rowCount():
            self.setRowCount(len(clip2paste)-1)
        self.addData(clip2paste, 0, 0)
        self.calcDiff()
        self.setColors()

    def openWorkFromTxt(self):
        s = QSettings("CMPiS","MikeCal")
        lastWorkFileDir = str(s.value("profileMike/lastWorkFileDir", "").toString())
        workFilename = QFileDialog.getOpenFileName(None, 'Working Profile file name', directory=lastWorkFileDir, filter='All files (*.*)')
        if workFilename:
            s.setValue("profileMike/lastWorkFileDir", dirname(str(workFilename)))
            workFile = open(workFilename, "r")
            rows = workFile.readlines()
            clip2paste = []
            for row in rows[1:]:
                temp = []
                items = re.findall(r"[\w.]+", row)
                if len(items)<=3: # we got river, km, wsel
                    clip2paste.append(items)
                else: # we got river, km, wsel AND correction
                    clip2paste.append(items[:3]+["", ""]+items[3:4])
            if len(clip2paste) >= self.rowCount():
                self.setRowCount(len(clip2paste))
            self.addData(clip2paste, 0, 0)
            self.calcDiff()
            self.setColors()
            workFile.close()





    def splitClipboard(self, clipText):
        tempList = []
        returnClip = []
        clipList = clipText.split("\n")
        for item in clipList:
            data = re.findall(r"[\w.]+", item)
            if len(data)>0:
                if data[0] == 'Water':
                    continue
            returnClip.append(data[:2]+data[3:4])
        return returnClip

    def copyCells(self):
        selRange  = self.selectedRanges()[0]
        topRow = selRange.topRow()
        bottomRow = selRange.bottomRow()
        rightColumn = selRange.rightColumn()
        leftColumn = selRange.leftColumn()
        clipStr = QString()
        for row in xrange(topRow, bottomRow+1):
            for col in xrange(leftColumn, rightColumn+1):
                cell = self.item(row, col)
                if cell:
                    clipStr.append(cell.text())
                else:
                    clipStr.append(QString(""))
                clipStr.append(QString("\t"))
            clipStr.chop(1)
            clipStr.append(QString("\r\n"))

        cb = QApplication.clipboard()
        cb.setText(clipStr)