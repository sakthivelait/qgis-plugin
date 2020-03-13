# -*- coding: utf-8 -*-
"""
/***************************************************************************
 indices
                                 A QGIS plugin
 for calculate indices
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2019-12-17
        git sha              : $Format:%H$
        copyright            : (C) 2019 by sakthi
        email                : sakthivel@gmail.com
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
#from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction,QFileDialog,QProgressBar
from qgis.core import QgsProject, Qgis, QgsRasterLayer
import processing,tempfile
from qgis.utils import iface


from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry

from .indices_tool import SATool


# Initialize Qt resources from file resources.py
from .resources import *

# Import the code for the dialog
from .indices_dialog import indicesDialog
import os.path
import time



class indices:
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
            'indices_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&indices')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        #self.first_start = None



        self.toolbar = self.iface.addToolBar(u'indices')
        self.toolbar.setObjectName(u'indices')



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
        return QCoreApplication.translate('indices', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
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
        self.dlg = indicesDialog()


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
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToRasterMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/indices/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'indices'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


#Custom functions.

    # updating dropdown list content
    def update_rasters_boxes(self):

        # clear lists
        self.clear_boxes(
                self.dlg.redBox,
                self.dlg.nirBox,
                self.dlg.swirBox
            )

        # shaping new content
        layers = list()
        layers.append("Not Set")
        layers = layers + [lay.name() for lay in self.iface.mapCanvas().layers()]

        # add new content to dropdown lists
        self.add_layers_to_raster_boxes(
            layers,
            self.dlg.redBox,
            self.dlg.nirBox,
            self.dlg.swirBox
        )

    # Adding a list of layers
    def add_layers_to_raster_boxes(self, layers, *boxes):
        for box in boxes:
            box.addItems(layers)

    def clear_boxes(self, *boxes):
        for box in boxes:
            box.clear()

    # method for selecting the resulting raster file
    def select_output_file(self):
        filename = QFileDialog.getSaveFileName(
            self.dlg, "Select output file ", "", '*.tif'
        )
        self.dlg.lineEdit.setText(filename[0])


  
    def on_ok(self):
        index_name = self.dlg.viBox.currentText()
        red_band = self.iface.mapCanvas().layers()[self.dlg.redBox.currentIndex() - 1]
        nir_band = self.iface.mapCanvas().layers()[self.dlg.nirBox.currentIndex() - 1]
        output = self.dlg.lineEdit.text()
        swir_band = self.iface.mapCanvas().layers()[self.dlg.swirBox.currentIndex() - 1]



        self.tool = SATool(
            index_name,
            red_band, nir_band, output,
            swir_band,
        )

        if self.tool.index == "NDVI":
            self.tool.calc_ndvi()
            if self.dlg.checkBox.isChecked():
                out = iface.addRasterLayer(output, "")
        elif self.tool.index == "RVI":
            self.tool.calc_rvi()
            if self.dlg.checkBox.isChecked():
                out = iface.addRasterLayer(output, "")
        elif self.tool.index == "DVI":
            self.tool.calc_dvi()
            if self.dlg.checkBox.isChecked():
                out = iface.addRasterLayer(output, "")
        elif self.tool.index == "IPVI":
            self.tool.calc_ipvi()
            if self.dlg.checkBox.isChecked():
                out = iface.addRasterLayer(output, "")
        elif self.tool.index == "NDWI":
            self.tool.calc_ndwi()
            if self.dlg.checkBox.isChecked():
                out = iface.addRasterLayer(output, "")
        elif self.tool.index == "NDBI":
            self.tool.calc_ndbi()
            if self.dlg.checkBox.isChecked():
                out = iface.addRasterLayer(output, "")



#Ended the custom functions.



    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginRasterMenu(
                self.tr(u'&indices'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar




    def run(self):
        """Run method that performs all the real work"""

        self.update_rasters_boxes()
        self.dlg.viBox.clear()
        self.dlg.viBox.addItems(["NDVI", "RVI","DVI","IPVI", "NDWI","NDBI"])

        self.dlg.lineEdit.clear()
        #connection to the select button
        self.dlg.outputButton.clicked.connect(self.select_output_file)
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            

            
            self.on_ok()
            
           
            self.iface.messageBar().pushMessage("output created Successfully", level=Qgis.Success, duration=3)            
            self.dlg.outputButton.clicked.disconnect(self.select_output_file)
            
                      