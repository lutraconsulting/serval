# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Serval,  A QGIS plugin


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

from __future__ import absolute_import


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    from .serval import Serval
    return Serval(iface)
