# -*- coding: utf-8 -*-
"""
/***************************************************************************
 serval,  A QGIS plugin


 Map tools for manipulating raster cell values

    begin            : 2015-12-30
    copyright        : (C) 2019 Radosław Pasiok for Lutra Consulting Ltd.
    email            : info@lutraconsulting.co.uk
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.PyQt.QtWidgets import QMessageBox
from qgis.core import QgsMessageLog, Qgis


class UserCommunication:
    """Class for communication with user"""
    
    def __init__(self, iface, context):
        self.iface = iface
        self.context = context
        
    def show_info(self, msg):
        QMessageBox.information(self.iface.mainWindow(), self.context, msg)
        
    def show_warn(self, msg):
        QMessageBox.warning(self.iface.mainWindow(), self.context, msg)
        
    def log_info(self, msg):
        QgsMessageLog.logMessage(msg, self.context, QgsMessageLog.INFO)
        
    def bar_error(self, msg):
        self.iface.messageBar().pushMessage(self.context, msg, level=Qgis.Critical)

    def bar_warn(self, msg, dur=5):
        self.iface.messageBar().pushMessage(self.context, msg, level=Qgis.Warning, duration=dur)
        
    def bar_info(self, msg, dur=5):
        self.iface.messageBar().pushMessage(self.context, msg, duration=dur)
