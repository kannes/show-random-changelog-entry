# -----------------------------------------------------------
# Copyright (C) Johannes Kröger
# based on qgis-minimal-plugin from Thomas Baumann
# -----------------------------------------------------------
# Licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# ---------------------------------------------------------------------

import random

from qgis.PyQt.QtCore import QTimer, QUrl
# no clue about the current state of QWebEngineView so good old webkit...
from qgis.PyQt.QtWebKit import QWebElement, QWebElementCollection
from qgis.PyQt.QtWebKitWidgets import QWebView

from qgis.core import Qgis, QgsMessageLog


def classFactory(iface):
    return RandomChangelogEntryPlugin(iface)


class RandomChangelogEntryPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.web_view = None
        self.has_been_shown = False

        self.iface.newProjectCreated.connect(self.run)

    def initGui(self):
        pass

    def unload(self):
        del self.web_view

    def run(self):
        if self.has_been_shown:
            return
        self.has_been_shown = True

        self.iface.messageBar().pushMessage(
            "RandomChangelogEntryPlugin", "Fetching Changelog...", level=Qgis.Info, duration=20,
        )
        qgis_version = Qgis.QGIS_VERSION_INT // 100  # -> 33400 -> 334

        changelog_url = QUrl(f"https://qgis.org/en/site/forusers/visualchangelog{qgis_version}/index.html")

        self.web_view = QWebView()
        self.web_view.setWindowTitle(f"Check out this fresh new feature of QGIS {qgis_version/100:1.2f}")
        self.web_view.setFixedWidth(750)  # fixed width to get the responsive view without side navigation

        # use signal of frame not webview via https://stackoverflow.com/a/8781111/4828720
        self.web_view.page().mainFrame().loadFinished.connect(self.show_random_changelog_entry)

        QgsMessageLog.logMessage("Fetching changelog...", "RandomChangelogEntryPlugin", level=Qgis.Info)
        self.web_view.load(changelog_url)

    def show_random_changelog_entry(self):
        QgsMessageLog.logMessage("Fetching changelog... Done!", "RandomChangelogEntryPlugin", level=Qgis.Info)

        # move window to center of QGIS window
        # if we do this immediately on plugin load, the QGIS window might not be initialized properly
        qgis_center_point = self.iface.mainWindow().geometry().center()
        view_geometry = self.web_view.geometry()
        view_geometry.moveCenter(qgis_center_point)
        self.web_view.setGeometry(view_geometry)

        page = self.web_view.page()
        frame = page.mainFrame()
        # actual changelog entry are within the changelog section and then within categorical sections
        sections_collection: QWebElementCollection = frame.findAllElements("section section section[id]")
        sections: list[QWebElement] = sections_collection.toList()
        QgsMessageLog.logMessage(f"Found {len(sections)} sections", "RandomChangelogEntryPlugin", level=Qgis.Info)
        random_section = random.choice(sections)
        random_section_id = random_section.attribute("id")
        QgsMessageLog.logMessage(
            f"Selected section {random_section_id!r}", "RandomChangelogEntryPlugin", level=Qgis.Info
        )
        frame.evaluateJavaScript(f"document.getElementById('{random_section_id}').scrollIntoView();")

        # ready to show the window
        # with timer to make sure scrolling has happened before showing
        QTimer.singleShot(1000, self.web_view.show)
