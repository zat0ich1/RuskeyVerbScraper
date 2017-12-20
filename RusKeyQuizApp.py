#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 10:39:40 2017

@author: eli
"""

import sys
import os
from PyQt4 import QtGui
from PyQt4 import QtCore
def mainWindow(verbList, formsList, audioFile):
    app =  QtGui.QApplication(sys.argv)
    QverbBrowser = QtGui.QWidget()
    QverbBrowser.setGeometry(100,100,850,800)
    # Grid layouts - main window is broken up into three sub grids nested within
    # a lager grid as follows:
    # |  1       |  2  |
    # |        3       |
    # subgrid 1 will contain the non past forms and info on aspect, etc. (nonPastBrowserGrid)
    # subgrid 2 will contain the past forms (pastBrowserGrid)
    # subgrid 3 will contain a list view with all verbs available, as well as
    # a list view of verbs selected for quiz and buttons to add verbs to proposed quiz
    QverbBrowserGrid = QtGui.QGridLayout()
    QnonPastBrowserGrid = QtGui.QGridLayout()
    QpastBrowserGrid = QtGui.QGridLayout()
    QquizSelectorGrid = QtGui.QgridLayout()
    QboldFont = QtGui.QFont
    QboldFont.setBold(True)
    QverbBrowserGrid.addWidget(QnonPastBrowserGrid, 1, 1, 1, 2)
    QverbBrowserGrid.addWidget(QpastBrowserGrid,1,2)
    QverbBrowserGrid.addWidget(QquizSelectorGrid,2,1,1,3)
    # ---------------------------------------------
    # configuring the nonPastForms areas
    # label:
    QnonPastFieldLabel = QtGui.QLabel("Non-Past Forms")
    QnonPastFieldLabel.setFont(QboldFont)
    QnonPastFieldLabel.setAlignment(QtCore.Qt.AlignCenter)
    QnonPastBrowserGrid.addWidget(QnonPastFieldLabel,1,1,1,4)
    # play audio button:
    QplayAudioButton = QtGui.QPushButton("Play Audio")
    QnonPastBrowserGrid.addWidget(QplayAudioButton,2,1,1,4)
    #Infinitive label and form
    QinfinitiveLabel = QtGui.QLabel("infinitive:")
    QinfinitiveHolder = QtGui.QLineEdit(formsList[0])
    QnonPastBrowserGrid.addWidget(QinfinitiveLabel,3,1,1,1)
    QnonPastBrowserGrid.addWidget(QinfinitiveHolder,3,2,1,1)
    #Aspect label and form

    nonPastBrowserGrid.addWidget()
    verbBrowser.setLayout(verbBrowserGrid)
    verbBrowser.setWindowTitle("RusKey Verb Browser")
    verbBrowser.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    window(['this','is','a','list'])

verbList = os.listdir('./verbs')
verbList.sort()
formsList = ['быть',
            'imperfective',
            1,
            'be',
            'бу́ду',
            'бу́дешь',
            'бу́дет',
            'бу́дем',
            'бу́дете',
            'будут',
            'бу́дь',
            'бу́дьте',
            'бы́л',
            'была́',
            'бы́ло',
            'бы́ли']
audioFile = './verbs/0001byt.mp3'
