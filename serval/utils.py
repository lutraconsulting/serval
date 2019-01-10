# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Serval
                                 A QGIS plugin
 Set Raster Values
                              -------------------
        begin                : 2015-12-30
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Radosław Pasiok
        email                : rpasiok@gmail.com
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


dtypes = {
    0: {'name': 'UnknownDataType'}, 
    1: {'name': 'Byte', 'atype': 'B',
        'min': 0, 'max': 255, 'dig': 0},
    2: {'name': 'UInt16', 'atype': 'H',
        'min': 0, 'max': 65535, 'dig': 0},
    3: {'name': 'Int16', 'atype': 'h',
        'min': -32768, 'max': 32767, 'dig': 0},
    4: {'name': 'UInt32', 'atype': 'I',
        'min': 0, 'max': 4294967295, 'dig': 0},
    5: {'name': 'Int32', 'atype': 'i',
        'min': -2147483648, 'max': 2147483647, 'dig': 0},
    6: {'name': 'Float32', 'atype': 'f',
        'min': -3.4e38, 'max': 3.4e38, 'dig': 4},   # max digs 5
    7: {'name': 'Float64', 'atype': 'd',
        'min': -1.7e308, 'max': 1.7e308, 'dig': 4},  # max digs 12
    8: {'name': 'CInt16'}, 
    9: {'name': 'CInt32'}, 
    10: {'name': 'CFloat32'}, 
    11: {'name': 'CFloat64'}, 
    12: {'name': 'ARGB32'}, 
    13: {'name': 'ARGB32_Premultiplied'}
}


def is_number(s):
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        return False


def icon_path(icon_filename):
    plugin_dir = os.path.dirname(__file__)
    return os.path.join(plugin_dir, 'icons', icon_filename)
