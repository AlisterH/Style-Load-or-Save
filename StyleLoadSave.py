# -*- coding: utf-8 -*-
"""
/***************************************************************************
 StyleLoadSave
                                 A QGIS plugin
 Load and Save Current vector Layer Style
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2023-05-12
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Giulio Fattori
        email                : g@g.com
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
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QToolBar

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
#from .StyleLoadSave_dialog import StyleLoadSaveDialog
import os.path

from qgis.core import Qgis, QgsMapLayer
from PyQt5 import QtCore, QtGui
import base64

load_icon = b'PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIGVuYWJsZS1iYWNrZ3JvdW5kPSJuZXcgLTQgLTQgMjQgMjQiIHZlcnNpb249IjEuMSIgdmlld0JveD0iLTQgLTQgMjQgMjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CiA8ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgwIC0xNikiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCI+CiAgPGcgdHJhbnNmb3JtPSJtYXRyaXgoLjc0MDA4IDAgMCAuNzgyOTMgLTMuODQxMyAtNzg1LjgpIiBmaWxsPSIjZmNkOTRmIiBzdHJva2U9IiNiMjlhMzciIHN0cm9rZS1saW5lam9pbj0icm91bmQiPgogICA8cGF0aCBkPSJtMS41IDEwNDcuNHYtMjIuNWg5djNoMTZ2MTkuNXoiLz4KICAgPHBhdGggZD0ibTEuNSAxMDQ3LjQgNC0xNmgyNWwtNCAxNnoiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgogIDwvZz4KICA8cGF0aCBkPSJtNi4wOTEgMjguNDE0cy0yLjUyMyAzLjc4My03LjU2OCA1LjA0NWMyLjI1OSAwLjAzODA1IDUuODAwNCAwLjAyNzAyIDguMDMwOS0xLjAwMDEgMS4yMjgzLTAuNTY1NjQgMi4wNTkxLTEuNDM5NCAyLjA1OTEtMi43ODI5eiIgZmlsbD0iIzQ4NDUzNyIgc3Ryb2tlPSIjMjQyMjFjIi8+CiAgPGcgZmlsbD0iIzgwMDAwMCIgc3Ryb2tlPSIjODg4YTg1IiBzdHJva2Utd2lkdGg9Ii43NSI+CiAgIDxwYXRoIGQ9Im05LjI0NCAyMi43MzkgMy43ODMgMi41MjItMy43ODMgMy43ODNzLTEuODA1LS4yMjMtMi41MjItMS4yNjFjLS43MTgtMS4wMzcgMi42LTQuOTY1IDIuNTIyLTUuMDQ0eiIvPgogICA8cGF0aCBkPSJtOS4yNDQgMjIuNzM5czcuMDgyLTcuNzk5IDguMTk3LTguMTk4YzEuMTE2LS4zOTgtMy42OTcgMTAuMTYyLTQuNDE0IDEwLjcycy0zLjA5Mi0xLjM3OS0zLjc4My0yLjUyMnoiLz4KICA8L2c+CiA8L2c+Cjwvc3ZnPgo='
save_icon = b'PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIGVuYWJsZS1iYWNrZ3JvdW5kPSJuZXcgLTQgLTQgMjQgMjQiIHZlcnNpb249IjEuMSIgdmlld0JveD0iLTQgLTQgMjQgMjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CiA8ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgwIC0xNikiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCI+CiAgPGcgdHJhbnNmb3JtPSJtYXRyaXgoLjkzNDU1IDAgMCAuODI5NTQgLTQuNDk3MiAxNS43NDEpIiBzdHJva2UtbGluZWNhcD0icm91bmQiPgogICA8cmVjdCB4PSIyLjQiIHk9IjEuNCIgd2lkdGg9IjE5LjIiIGhlaWdodD0iMjAuNSIgcng9IjEuODg5IiByeT0iMS41IiBmaWxsPSIjNmQ5N2M0IiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIHN0cm9rZT0iIzQxNWE3NSIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgc3Ryb2tlLXdpZHRoPSIuOCIvPgogICA8ZyBzdHJva2U9IiM2NjYiPgogICAgPHJlY3QgeD0iNSIgeT0iMiIgd2lkdGg9IjE0IiBoZWlnaHQ9IjkiIHJ4PSIuNSIgZmlsbD0iI2VkZWRlZCIgZmlsbC1ydWxlPSJldmVub2RkIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBzdHJva2Utd2lkdGg9Ii41Ii8+CiAgICA8cGF0aCBkPSJtNyA0LjVoMTAiIGZpbGw9Im5vbmUiLz4KICAgIDxwYXRoIGQ9Im02LjAxIDE0LjUxN2gxMS45OXY2Ljk4M2gtMTEuOTl6IiBmaWxsPSIjZWRlZGVkIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIHN0cm9rZS13aWR0aD0iLjYiLz4KICAgPC9nPgogICA8cGF0aCBkPSJtNy4wMDkgMTUuNDFoMy45OTN2NC45NjloLTMuOTkzeiIgZmlsbD0iIzQxNWE3NSIgZmlsbC1ydWxlPSJldmVub2RkIiBzdHJva2U9IiNlNmU2ZTYiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIHN0cm9rZS13aWR0aD0iLjk5NiIvPgogICA8cGF0aCBkPSJtNyA2LjVoMTBtLTEwIDJoMTAiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzY2NiIvPgogIDwvZz4KICA8cGF0aCBkPSJtNi4wOTEgMjguNDE0cy0yLjUyMyAzLjc4My03LjU2OCA1LjA0NWMyLjI1OSAwLjAzODA1IDUuODAwNCAwLjAyNzAyIDguMDMwOS0xLjAwMDEgMS4yMjgzLTAuNTY1NjQgMi4wNTkxLTEuNDM5NCAyLjA1OTEtMi43ODI5eiIgZmlsbD0iIzQ4NDUzNyIgc3Ryb2tlPSIjMjQyMjFjIi8+CiAgPGcgZmlsbD0iIzgwMDAwMCIgc3Ryb2tlPSIjODg4YTg1IiBzdHJva2Utd2lkdGg9Ii43NSI+CiAgIDxwYXRoIGQ9Im05LjI0NCAyMi43MzkgMy43ODMgMi41MjItMy43ODMgMy43ODNzLTEuODA1LS4yMjMtMi41MjItMS4yNjFjLS43MTgtMS4wMzcgMi42LTQuOTY1IDIuNTIyLTUuMDQ0eiIvPgogICA8cGF0aCBkPSJtOS4yNDQgMjIuNzM5czcuMDgyLTcuNzk5IDguMTk3LTguMTk4YzEuMTE2LS4zOTgtMy42OTcgMTAuMTYyLTQuNDE0IDEwLjcycy0zLjA5Mi0xLjM3OS0zLjc4My0yLjUyMnoiLz4KICA8L2c+CiA8L2c+Cjwvc3ZnPgo='



class StyleLoadSave:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'StyleLoadSave_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&StyleLoadSave')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('StyleLoadSave', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=False,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            # self.iface.addToolBarIcon(action)
            
            # Adds plugin icon to LayerThreeDock toolbar
            self.iface.layerTreeView().parent().findChildren(QToolBar)[0].addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        #icon_path = ':/plugins/StyleLoadSave/icon.png'
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(QtCore.QByteArray.fromBase64(load_icon))
        icon_path = QIcon(pixmap)
        
        self.add_action(
            icon_path,
            text=self.tr(u'Load Default Style'),
            callback=self.load_Style,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True
        
        #icon_path = ':/plugins/StyleLoadSave/icon.png'
        #pixmap = QtGui.QPixmap()
        pixmap.loadFromData(QtCore.QByteArray.fromBase64(save_icon))
        icon_path = QIcon(pixmap)
        
        self.add_action(
            icon_path,
            text=self.tr(u'Save Default Style'),
            callback=self.save_Style,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&StyleLoadSave'),
                action)
            #self.iface.removeToolBarIcon(action)
            self.iface.layerTreeView().parent().findChildren(QToolBar)[0].removeAction(action)


    # def run(self):
        # """Run method that performs all the real work"""

        # # Create the dialog with elements (after translation) and keep reference
        # # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        # if self.first_start == True:
            # self.first_start = False
            # self.dlg = StyleLoadSaveDialog()

        # # show the dialog
        # self.dlg.show()
        # # Run the dialog event loop
        # result = self.dlg.exec_()
        # # See if OK was pressed
        # if result:
            # # Do something useful here - delete the line containing pass and
            # # substitute with your code.
            # pass
            
            
    def load_Style(self):
        layer = self.iface.activeLayer()
        if layer and layer.isSpatial() and layer.type() in [QgsMapLayer.VectorLayer, QgsMapLayer.RasterLayer, QgsMapLayer.MeshLayer]:
            layer.loadDefaultStyle()
            layer.emitStyleChanged()
            layer.triggerRepaint()
        else:
            self.iface.messageBar().pushMessage(
                "Error:",
                "Missing or Not Spatial Layer",
                level=Qgis.Warning, duration=3)


    def save_Style(self):
        if self.iface.activeLayer() and self.iface.activeLayer().isSpatial():
            self.iface.activeLayer().saveDefaultStyle()
        else:
            self.iface.messageBar().pushMessage(
                "Error:",
                "Missing or Not Spatial Layer",
                level=Qgis.Warning, duration=3)