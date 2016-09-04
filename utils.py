# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MMTools
                                 A QGIS plugin
        Print composer, mask and markers creation
                              -------------------
        begin                : 2016-08-09
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Lutra
        email                : info@lutraconsulting.co.uk
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

import os.path
import ConfigParser

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    

def read_ini_par(file, section, parameter):
    # Get the email address from the configuration file file
    parser = ConfigParser.ConfigParser()
    parser.read(file)
    return parser.get(section, parameter)