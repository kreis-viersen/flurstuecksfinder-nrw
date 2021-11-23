# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Flurstücksfinder NRW
                                 A QGIS plugin
 With this plugin Flurstücke can be searched on a WFS
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-03-03
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Kreis Viersen
        email                : open@kreis-viersen.de
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load FlurstuecksFinderNRW class from file FlurstuecksFinderNRW.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .flurstuecks_finder_nrw import FlurstuecksFinderNRW
    return FlurstuecksFinderNRW(iface)