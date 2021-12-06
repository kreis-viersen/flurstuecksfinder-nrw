#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import socket
import sys
import xml.etree.cElementTree as ET
import urllib
import time
import warnings
from PyQt5.QtWidgets import QMessageBox

warnings.filterwarnings(
    action='ignore',
    module='subprocess'
)

class StartJosm(object):
    def __init__(self, parent):
        # super(StartJosm, self).__init__(parent)
        self.c_dir = os.path.dirname(os.path.realpath(__file__))
        self.homepath = os.path.expanduser("~")
        if hasattr(parent, 'iface'):
            self.parent = parent.iface.mainWindow()
        else:
            self.parent = parent

    def josmSearchPath(self):
        ''' Funktion zur Suche des JOSM Pfade '''
        if sys.platform.startswith("linux"):
            app_dir = "/usr/share/josm/"
            cfg_dir = os.path.join(self.homepath, ".config/JOSM")
        elif sys.platform.startswith("win"):
            app_dir = r'C:\Program Files (x86)\JOSM'
            cfg_dir = os.path.join(self.homepath, r"AppData\Roaming\JOSM")

        # Legt den Pfad zum JOSM Programm fest
        # Mögliche Namen des JOSM Programms
        josm_exe = ["josm-tested.jar", "josm.exe", "josm.jnlp", "josm.jar"]
        josm_app_path = None

        # Schleife über die JOSM Programm. Variable josm_app_path wird belegt
        # wenn der Pfad zur Datei gültig ist
        for exe in josm_exe:
            if os.path.isfile(os.path.join(app_dir, exe)):
                josm_app_path = os.path.join(app_dir, exe)
            else:
                pass

        # Legt den Pfad zur JOSM Config fest
        josm_cfg_path = None
        if os.path.isfile(os.path.join(cfg_dir, "preferences.xml")):
            josm_cfg_path = os.path.join(cfg_dir, "preferences.xml")

        return(josm_app_path, josm_cfg_path)

    def josmVarSet(self):
        ''' Überprüft ob die benötigte Funktion "JOSM Remote" in der Config-Datei aktiviert ist und setzt Sie wenn nötig '''
        _, josm_cfg_path = self.josmSearchPath()
        josmVarSet = False
        if josm_cfg_path:
            if os.path.isfile(josm_cfg_path):
                tree = ET.parse(josm_cfg_path)
                ET.register_namespace(
                    '', 'http://josm.openstreetmap.de/preferences-1.0')
                root = tree.getroot()
                string = root.find(
                    "{http://josm.openstreetmap.de/preferences-1.0}tag[@key='remotecontrol.enabled']")
                if string is None or string.attrib["value"] == "false":
                    message = f'JOSM Remote ist nicht aktiviert. <br>Bitte folgen Sie den Schritten <a href="https://josm.openstreetmap.de/wiki/Help/Preferences/RemoteControl">dieser Anleitung</a> und bestätigen Sie diesen Dialog mit OK. Klicken Sie danach erneut auf den JOSM Knopf'
                    reply = QMessageBox.information(self.parent, "JOSM Remote", message, QMessageBox.Ok, QMessageBox.Ok)
                    if reply == QMessageBox.Yes:
                        self.josmVarSet()
                else:
                    josmVarSet = True
                return(josmVarSet)

    def josmPortOpen(self):
        ''' Prüft, ob der JOSM Port geöffnet ist '''
        ip = "127.0.0.1"
        port = 8111
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            result = s.connect_ex((ip, port))
            if result == 0:
                return True
            else:
                return False

    def josmStarted(self):
        ''' Funktion versucht JOSM zu öffnen '''
        josm_app_path, _ = self.josmSearchPath()
        if josm_app_path:
            if os.path.isfile(josm_app_path):  # Wenn Datei vorhanden
                reply = QMessageBox.question(self.parent, "JOSM Starten", "Soll JOSM jetzt gestartet werden?", QMessageBox.Yes|QMessageBox.No)
                if reply == QMessageBox.Yes:
                    try:
                        if sys.platform.startswith("linux"):
                            param = ['java', '-jar', josm_app_path]
                        elif sys.platform.startswith("win"):
                            param = [josm_app_path]
                        subprocess.Popen(param)
                        while self.josmPortOpen() is False:
                            time.sleep(0.1)
                        return True
                    except:
                        return False

    def openJosmApp(self, xmin, xmax, ymin, ymax):
        ''' Funktion zum Aufrufen von JOSM '''
        ''' Wenn JOSM NICHT offen ist, wird versucht die Programm zu starten '''
        ''' Wenn Port offen und Config richtig '''
        if self.josmVarSet() is True:
            if self.josmPortOpen() is False:
                if self.josmStarted() is False:
                    pass
            # # if self.josmPortOpen() is not True:
            # #     pass
            # if self.josmStarted() is not True:
            #     pass

            try:
                proxy_handler = urllib.request.ProxyHandler({})
                opener = urllib.request.build_opener(proxy_handler)
                url = f'http://localhost:8111/load_and_zoom?left={xmin}&right={xmax}&bottom={ymin}&top={ymax}'
                request = opener.open(url)
                result_request = opener.open(url, timeout=3)
                result = result_request.read()
                result = result.decode('utf8')
            except IOError:
                pass
