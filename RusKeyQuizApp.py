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

class QtDisplay(QtGui.QLineEdit): #custom version of QLineEdit class that disables editing by default
    def __init__(self):
        QtGui.QLineEdit.__init__(self)
        QtGui.QLineEdit.setReadOnly(self,True)

class QtSectionLabel(QtGui.QLabel): #custom version of QLabel class that center aligns, bolds, and sets vertical policy to fixed by default
    def __init__(self, text):
        QtGui.QLabel.__init__(self, text)
        QboldFont = QtGui.QFont()
        QboldFont.setBold(True)
        self.setFont(QboldFont)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Fixed)

class QtVFixedLabel(QtGui.QLabel): #custom version of the QLabel class that sets vertical policy to fixed by default
    def __init__(self,text):
        QtGui.QLabel.__init__(self, text)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Fixed)

def mainWindow():
    app =  QtGui.QApplication(sys.argv)
    QverbBrowser = QtGui.QWidget()
    QverbBrowser.setGeometry(100,100,800,800)
    #--------------------------------------------
    # GRID LAYOUT
    #--------------------------------------------
    # The grid layout consists of three subgrids inside of 5 main grid as follows. Some of these sub grids are further subdivided
    #    ___________
    #   | np   | p&i|     NP - non-past indicative forms
    #   |______|____|     P&I - past and imperative forms
    #   |vb | btn|q |     VB - verb browser (shows available verbs)
    #   |___|____|__|     btn - buttons to add verbs to quiz
    #                     q - list of verbs selected for quiz
    QverbBrowserGrid = QtGui.QGridLayout() #main layout
    # ---------------------------------------------
    # NON PAST FORMS AREA
    #----------------------------------------------
    #    ___________
    #   |*NP***|    |     NP - non-past indicative forms - QNPISubGrid
    #   |______|____|
    #   |   |    |  |
    #   |___|____|__|
    #
    QNPISubGrid = QtGui.QGridLayout()
    QverbBrowserGrid.addLayout(QNPISubGrid, 0, 0, 1, 2)
    #   this area is further subdivided as follows
    # __________________________
    # |                        |
    # |                        |
    # |      QinfoSubGrid      |
    # |________________________|
    # |                        |
    # | QNPIFormsSubGrid       |
    # |________________________|
    #
    QinfoSubGrid = QtGui.QGridLayout()
    QNPIFormsSubGrid = QtGui.QGridLayout()
    QNPISubGrid.addLayout(QinfoSubGrid,0,0,2,1)
    QNPISubGrid.addLayout(QNPIFormsSubGrid,3,0,1,1)

    #----------------------------------------------
    # NON PAST INDICATIVE AREA LABEL:
    #----------------------------------------------
    QnonPastPaneLabel = QtSectionLabel("Non-Past Indicative Forms")
    QinfoSubGrid.addWidget(QnonPastPaneLabel,0,0,1,4)
    # ----------------------------------------------
    # PLAY AUDIO BUTTON:
    #-----------------------------------------------
    QplayAudioButton = QtGui.QPushButton("Play Audio")
    QinfoSubGrid.addWidget(QplayAudioButton,1,2,1,2)
    #-----------------------------------------------
    # INFINITIVE LABEL AND BOX
    #-----------------------------------------------
    QinfinitiveLabel = QtVFixedLabel("Infinitive:")
    QinfinitiveBox = QtDisplay()
    QinfoSubGrid.addWidget(QinfinitiveLabel,1,0,1,1)
    QinfoSubGrid.addWidget(QinfinitiveBox,1,1,1,1)

    #-----------------------------------------------
    # MEANING LABEL AND BOX
    #-----------------------------------------------
    QmeaningLabel = QtVFixedLabel("Meaning:")
    QmeaningBox = QtDisplay()
    QinfoSubGrid.addWidget(QmeaningLabel,2,0,1,1)
    QinfoSubGrid.addWidget(QmeaningBox,2,1,1,3)

    #-----------------------------------------------
    # ASPECT LABEL AND BOX
    #-----------------------------------------------
    QaspectLabel = QtVFixedLabel("Aspect:")
    QaspectBox = QtDisplay()
    QinfoSubGrid.addWidget(QaspectLabel,3,0,1,1)
    QinfoSubGrid.addWidget(QaspectBox,3,1,1,1)
    #-----------------------------------------------
    # FEQUENCY LABEL AND BOX
    #-----------------------------------------------
    QfrequencyLabel = QtVFixedLabel("Frequency Number:")
    QfrequencyBox = QtDisplay()
    QinfoSubGrid.addWidget(QfrequencyLabel,3,2,1,1)
    QinfoSubGrid.addWidget(QfrequencyBox,3,3,1,1)
    #-----------------------------------------------
    # 1ST PERSON SINGULAR INDICATIVE
    #-----------------------------------------------
    QfirstSgLabel = QtVFixedLabel("1st Person Singular:")
    QfirstSgBox = QtDisplay()
    QNPIFormsSubGrid.addWidget(QfirstSgLabel,0,0,1,1)
    QNPIFormsSubGrid.addWidget(QfirstSgBox,1,0,1,1)
    #-----------------------------------------------
    # 2ND PERSON SINGULAR INDICATIVE
    #-----------------------------------------------
    QsecondSgLabel = QtVFixedLabel("2nd Person Singular:")
    QsecondSgBox = QtDisplay()
    QNPIFormsSubGrid.addWidget(QsecondSgLabel,2,0,1,1)
    QNPIFormsSubGrid.addWidget(QsecondSgBox,3,0,1,1)
    #-----------------------------------------------
    # 3RD PERSON SINGULAR INDICATIVE
    #-----------------------------------------------
    QthirdSgLabel = QtVFixedLabel("3rd Person Singular:")
    QthirdSgBox = QtDisplay()
    QNPIFormsSubGrid.addWidget(QthirdSgLabel,4,0,1,1)
    QNPIFormsSubGrid.addWidget(QthirdSgBox,5,0,1,1)
    #-----------------------------------------------
    # 1ST PERSON PLURAL INDICATIVE
    #-----------------------------------------------
    QfirstPlLabel = QtVFixedLabel("1st Person Plural:")
    QfirstPlBox = QtDisplay()
    QNPIFormsSubGrid.addWidget(QfirstPlLabel,0,2,1,1)
    QNPIFormsSubGrid.addWidget(QfirstPlBox,1,2,1,1)
    #-----------------------------------------------
    # 2ND PERSON PLURAL INDICATIVE
    #-----------------------------------------------
    QsecondPlLabel = QtVFixedLabel("2nd Person Plural:")
    QsecondPlBox = QtDisplay()
    QNPIFormsSubGrid.addWidget(QsecondPlLabel,2,2,1,1)
    QNPIFormsSubGrid.addWidget(QsecondPlBox,3,2,1,1)
    #-----------------------------------------------
    # 3rd PERSON PLURAL INDICATIVE
    #-----------------------------------------------
    QthirdPlLabel = QtVFixedLabel("3rd Person Plural:")
    QthirdPlBox = QtDisplay()
    QNPIFormsSubGrid.addWidget(QthirdPlLabel,4,2,1,1)
    QNPIFormsSubGrid.addWidget(QthirdPlBox,5,2,1,1)




    # ---------------------------------------------
    # PAST AND IMPERATIVE FORMS AREA
    #----------------------------------------------
    #    ___________
    #   |      |P&I*|     P&I - Past and Imperative Forms - QPastSubGrid
    #   |______|____|
    #   |   |    |  |
    #   |___|____|__|
    #
    QPastSubGrid = QtGui.QGridLayout()
    QverbBrowserGrid.addLayout(QPastSubGrid,0,2,1,1)
    #----------------------------------------------
    # CURRENT USER DISPLAY
    #----------------------------------------------
    QuserLabel = QtVFixedLabel('Current User:')
    QuserBox = QtDisplay()
    QPastSubGrid.addWidget(QuserLabel,0,0,1,1)
    QPastSubGrid.addWidget(QuserBox,0,1,1,1)
    #----------------------------------------------
    # DATE STUDIED DISPLAY
    #----------------------------------------------
    QdateLabel = QtVFixedLabel('Date verb last studied:')
    QdateDisplay = QtDisplay()
    QPastSubGrid.addWidget(QdateLabel,1,0,1,1)
    QPastSubGrid.addWidget(QdateDisplay,1,1,1,1)
    #----------------------------------------------
    # PAST AND IMPERATIVE AREA LABEL:
    #----------------------------------------------
    QPastPaneLabel = QtSectionLabel("Imperative and Past Forms")
    QPastSubGrid.addWidget(QPastPaneLabel,2,0,1,2)
    #-----------------------------------------------
    # IMPERATIVE SINGULAR
    #-----------------------------------------------
    QimperativeSgLabel = QtVFixedLabel("Imperative Singular:")
    QimperativeSgBox = QtDisplay()
    QPastSubGrid.addWidget(QimperativeSgLabel,3,0,1,1)
    QPastSubGrid.addWidget(QimperativeSgBox,3,1,1,1)
    #-----------------------------------------------
    # IMPERATIVE PLURAL
    #-----------------------------------------------
    QimperativePlLabel = QtVFixedLabel("Imperative Plural:")
    QimperativePlBox = QtDisplay()
    QPastSubGrid.addWidget(QimperativePlLabel,4,0,1,1)
    QPastSubGrid.addWidget(QimperativePlBox,4,1,1,1)
    #-----------------------------------------------
    # PAST MASCULINE
    #-----------------------------------------------
    QpastMascLabel = QtVFixedLabel("Past Masculine:")
    QpastMascBox = QtDisplay()
    QPastSubGrid.addWidget(QpastMascLabel,5,0,1,1)
    QPastSubGrid.addWidget(QpastMascBox,5,1,1,1)
    #-----------------------------------------------
    # PAST FEMININE
    #-----------------------------------------------
    QpastFemLabel = QtVFixedLabel("Past Feminine:")
    QpastFemBox = QtDisplay()
    QPastSubGrid.addWidget(QpastFemLabel,6,0,1,1)
    QPastSubGrid.addWidget(QpastFemBox,6,1,1,1)
    #-----------------------------------------------
    # PAST NEUTER
    #-----------------------------------------------
    QpastNeutLabel = QtVFixedLabel("Past Neuter:")
    QpastNeutBox = QtDisplay()
    QPastSubGrid.addWidget(QpastNeutLabel,7,0,1,1)
    QPastSubGrid.addWidget(QpastNeutBox,7,1,1,1)
    #-----------------------------------------------
    # PAST PLURAL
    #-----------------------------------------------
    QpastPlLabel = QtVFixedLabel("Past Plural:")
    QpastPlBox = QtDisplay()
    QPastSubGrid.addWidget(QpastPlLabel,8,0,1,1)
    QPastSubGrid.addWidget(QpastPlBox,8,1,1,1)

    #-----------------------------------------------
    # BOTTOM SECIONS
    #-----------------------------------------------
    #    ___________
    #   |      |    |     QbottomGrid - houses the three subdivisions of the bottom sections
    #   |______|____|
    #   |***********|
    #   |___________|
    #
    QbottomGrid = QtGui.QGridLayout()
    QverbBrowserGrid.addLayout(QbottomGrid,1,0,1,3)
    #-----------------------------------------------
    # VERB BROWSER AREA
    #-----------------------------------------------
    #    ___________
    #   |      |    |
    #   |______|____|
    #   |vb*|    |  |     VB - verb browser (shows available verbs)
    #   |___|____|__|
    #
    #-----------------------------------------------
    QverbListGrid = QtGui.QGridLayout()
    QbottomGrid.addLayout(QverbListGrid,0,0,1,1)
    QverbListLabel = QtSectionLabel("Browse Available Verbs")
    QverbList = QtGui.QListWidget()
    QverbListGrid.addWidget(QverbListLabel,0,0,1,1)
    QverbListGrid.addWidget(QverbList,1,0,1,1)
    #------------------------------------------------
    #    ___________
    #   |      |    |
    #   |______|____|
    #   |   | btn|  |
    #   |___|____|__|     btn - buttons to add verbs to quiz
    #
    #------------------------------------------------
    QbuttonAreaGrid = QtGui.QGridLayout()
    QbottomGrid.addLayout(QbuttonAreaGrid,0,1,1,1)
    QdisplayVerbBtn = QtGui.QPushButton("View Conjugation")
    QautoQuizBtn = QtGui.QPushButton("Quiz on Most Overdue Items (auto)")
    QcustomQuizBtn = QtGui.QPushButton("Quiz on Custom List -->")
    QaddToListBtn = QtGui.QPushButton("-- Add to Quiz List -->")
    QremoveFromListBtn = QtGui.QPushButton("<-- Remove from Quiz List --")
    QbuttonAreaGrid.addWidget(QdisplayVerbBtn,0,0,1,1)
    QbuttonAreaGrid.addWidget(QautoQuizBtn,1,0,1,1)
    QbuttonAreaGrid.addWidget(QcustomQuizBtn,2,0,1,1)
    QbuttonAreaGrid.addWidget(QaddToListBtn,3,0,1,1)
    QbuttonAreaGrid.addWidget(QremoveFromListBtn,4,0,1,1)
    #-------------------------------------------------
    #    ___________
    #   |      |    |
    #   |______|____|
    #   |   |    | q|
    #   |___|____|__|
    #                     q - list of verbs selected for custom quiz
    #-------------------------------------------------
    QcustomQuizGrid = QtGui.QGridLayout()
    QbottomGrid.addLayout(QcustomQuizGrid,0,2,1,1)
    QcustomQuizLabel = QtSectionLabel("Custom Quiz List")
    QcustomQuizList = QtGui.QListWidget()
    QcustomQuizGrid.addWidget(QcustomQuizLabel,0,0,1,1)
    QcustomQuizGrid.addWidget(QcustomQuizList,1,0,1,1)

    QverbBrowser.setLayout(QverbBrowserGrid)
    QverbBrowser.setWindowTitle("RusKey Verb Browser")
    QverbBrowser.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    mainWindow()

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
