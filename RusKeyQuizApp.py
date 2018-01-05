#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 10:39:40 2017

@author: eli
"""

import sys
import os
import shelve
import random
from playsound import playsound
from ShelveVerbs import verb
from PyQt4 import QtGui
from PyQt4 import QtCore

class QtDisplay(QtGui.QLineEdit): #custom version of QLineEdit class that disables editing by default
    def __init__(self):
        QtGui.QLineEdit.__init__(self)
        QtGui.QLineEdit.setReadOnly(self,True)
class QtDisplayLong(QtGui.QLabel): #custom version of QLabel class that wraps by default (for display of meaning)
    def __init__(self):
        QtGui.QLabel.__init__(self)
        self.setWordWrap(True)



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
    QmainWindowObj = QtGui.QMainWindow()
    QverbBrowser = QtGui.QWidget()
    with shelve.open('./verbs/verbsDB') as verbShelf:
        print(verbShelf['users'])
        user = changeUserMsgBox(QverbBrowser, verbShelf['users']) #creates a dialog box for choosing a user
        if user not in verbShelf['users']:
            temp = []
            for u in verbShelf['users']:
                temp.append(u)
            temp.append(user)
            verbShelf['users'] = temp #add user to users item in verbShelf (store user permanently if not already stored)
    QmainWindowObj.setGeometry(100,100,800,800)
    QmainMenu = QmainWindowObj.menuBar()
    QfileMenu = QmainMenu.addMenu("File")
    QfileMenuAbout = QtGui.QAction("About", QmainMenu)
    QfileMenu.addAction(QfileMenuAbout)
    def aboutAction():
        QaboutWindow = QtGui.QMessageBox()
        QaboutWindow.setGeometry(150,150,300,300)
        QaboutWindow.setText("RusKey is an opensource project developed by Eli Ginsburg-Marcy. The examples, conjugations, and frequency rankings it contains are derived from data scraped from en.openrussian.org")
        QaboutWindow.setWindowTitle("About RusKey")
        QaboutWindow.setIcon(QtGui.QMessageBox.Information)
        QaboutWindow.setStandardButtons(QtGui.QMessageBox.Close)
        QaboutWindow.exec_()
    QfileMenuAbout.triggered.connect(aboutAction)
    QfileMenuManageUsers = QtGui.QAction("Manage Users", QmainMenu)
    QfileMenu.addAction(QfileMenuManageUsers)
    def manageUsers():
        QmanageUsersWindow = QtGui.QWidget(QmainWindowObj)
        QmanageUsersWindow.setWindowFlags(QtCore.Qt.Window)
        print(QtCore.Qt.Window)
        QmanageUsersWindow.setGeometry(150,150,400,400)
        QmanageUsersGrid = QtGui.QGridLayout()
        QchangeUserBtnMgUsers = QtGui.QPushButton("Change to Selected User")
        QdeleteUserBtn = QtGui.QPushButton("Delete Selected User")
        QuserList = QtGui.QListWidget()
        with shelve.open('./verbs/verbsDB') as verbShelf:
            userList = []
            for u in verbShelf['users']:
                userList.append(u)
            userList.sort()
            QuserList.addItems(userList)
        QmanageUsersGrid.addWidget(QchangeUserBtnMgUsers)
        QmanageUsersGrid.addWidget(QdeleteUserBtn)
        QmanageUsersGrid.addWidget(QuserList)
        QmanageUsersWindow.setLayout(QmanageUsersGrid)
        QmanageUsersWindow.show()
        QuserList.setCurrentRow(0)
    QfileMenuManageUsers.triggered.connect(manageUsers)
    QfileMenuQuit = QtGui.QAction("Quit", QmainMenu)
    QfileMenu.addAction(QfileMenuQuit)
    QfileMenuQuit.setShortcut("Ctrl+Q")


    #--------------------------------------------
    # GRID LAYOUT
    #--------------------------------------------
    # The grid layout consists of three subgrids inside of 5 main grid as follows. Some of these sub grids are further subdivided
    #    ___________
    #   | np   | p&i|     NP - non-past indicative forms
    #   |______|____|     P&I - past and imperative forms
    #   |___ex______|     ex - dynamically allocated space for example sentences
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
    QmeaningBox = QtDisplayLong()
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
#
#
#
    #----------------------------------------------
    # PAST AND IMPERATIVE AREA LABEL:
    #----------------------------------------------
    QPastPaneLabel = QtSectionLabel("Imperative and Past Forms")
    QPastSubGrid.addWidget(QPastPaneLabel,0,0,1,2)
    #-----------------------------------------------
    # IMPERATIVE SINGULAR
    #-----------------------------------------------
    QimperativeSgLabel = QtVFixedLabel("Imperative Singular:")
    QimperativeSgBox = QtDisplay()
    QPastSubGrid.addWidget(QimperativeSgLabel,1,0,1,1)
    QPastSubGrid.addWidget(QimperativeSgBox,1,1,1,1)
    #-----------------------------------------------
    # IMPERATIVE PLURAL
    #-----------------------------------------------
    QimperativePlLabel = QtVFixedLabel("Imperative Plural:")
    QimperativePlBox = QtDisplay()
    QPastSubGrid.addWidget(QimperativePlLabel,2,0,1,1)
    QPastSubGrid.addWidget(QimperativePlBox,2,1,1,1)
    #-----------------------------------------------
    # PAST MASCULINE
    #-----------------------------------------------
    QpastMascLabel = QtVFixedLabel("Past Masculine:")
    QpastMascBox = QtDisplay()
    QPastSubGrid.addWidget(QpastMascLabel,3,0,1,1)
    QPastSubGrid.addWidget(QpastMascBox,3,1,1,1)
    #-----------------------------------------------
    # PAST FEMININE
    #-----------------------------------------------
    QpastFemLabel = QtVFixedLabel("Past Feminine:")
    QpastFemBox = QtDisplay()
    QPastSubGrid.addWidget(QpastFemLabel,4,0,1,1)
    QPastSubGrid.addWidget(QpastFemBox,4,1,1,1)
    #-----------------------------------------------
    # PAST NEUTER
    #-----------------------------------------------
    QpastNeutLabel = QtVFixedLabel("Past Neuter:")
    QpastNeutBox = QtDisplay()
    QPastSubGrid.addWidget(QpastNeutLabel,5,0,1,1)
    QPastSubGrid.addWidget(QpastNeutBox,5,1,1,1)
    #-----------------------------------------------
    # PAST PLURAL
    #-----------------------------------------------
    QpastPlLabel = QtVFixedLabel("Past Plural:")
    QpastPlBox = QtDisplay()
    QPastSubGrid.addWidget(QpastPlLabel,6,0,1,1)
    QPastSubGrid.addWidget(QpastPlBox,6,1,1,1)

    #-----------------------------------------------
    # DYNAMICALLY ALLOCATED SPACE FOR EXAMPLES - this holder will be populated by a displayVerb function, since the number of examples
    # varies from verb to verb
    #-----------------------------------------------
    QexamplesGrid = QtGui.QGridLayout()
    QverbBrowserGrid.addLayout(QexamplesGrid,1,0,1,3)

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
    QverbBrowserGrid.addLayout(QbottomGrid,2,0,1,3)
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
    #----------------------------------------------
    # DATE STUDIED DISPLAY
    #----------------------------------------------
    QdateLabel = QtVFixedLabel('Due date:')
    QdateDisplay = QtDisplay()
    QverbListGrid.addWidget(QdateLabel,0,0,1,1)
    QverbListGrid.addWidget(QdateDisplay,0,1,1,1)
    QverbListGrid.addWidget(QverbListLabel,1,0,1,2)
    QverbListGrid.addWidget(QverbList,2,0,1,2)
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
    QchangeUserBtn = QtGui.QPushButton("Change User")
    QautoQuizBtn = QtGui.QPushButton("Quiz on Most Overdue Items (auto)")
    QcustomQuizBtn = QtGui.QPushButton("Quiz on Custom List -->")
    QaddToListBtn = QtGui.QPushButton("-- Add to Quiz List -->")
    QremoveFromListBtn = QtGui.QPushButton("<-- Remove from Quiz List --")
    QbuttonAreaGrid.addWidget(QchangeUserBtn,0,0,1,1)
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
    #----------------------------------------------
    # CURRENT USER DISPLAY
    #----------------------------------------------
    QuserLabel = QtVFixedLabel('Current User:')
    QuserBox = QtDisplay()
    QcustomQuizGrid.addWidget(QuserLabel,0,0,1,1)
    QcustomQuizGrid.addWidget(QuserBox,0,1,1,1)
    QcustomQuizGrid.addWidget(QcustomQuizLabel,1,0,1,2)
    QcustomQuizGrid.addWidget(QcustomQuizList,2,0,1,2)

    QverbBrowser.setLayout(QverbBrowserGrid)
    QmainWindowObj.setWindowTitle("RusKey Verb Browser")
    QmainWindowObj.setCentralWidget(QverbBrowser)
    QmainWindowObj.show()
    QuserBox.setText(user)
    verbs = getSortedVerbList(user) #load the verb list in the relevant due date order for user
    QverbList.addItems(verbs) #add the verbs in order to the QListWidget
    QverbList.setCurrentRow(0) #select the first row by default
    def populateVerb(verbKey): #function to update conjugation display when new verb in QverbList is selected
        with shelve.open('./verbs/verbsDB') as verbShelf:
            targetVerb = verbShelf[verbKey]
            QinfinitiveBox.setText(targetVerb.get_infinitive())
            QmeaningBox.setText(targetVerb.get_meaning())
            QaspectBox.setText(targetVerb.get_aspect())
            QfrequencyBox.setText(targetVerb.get_frequencyRank())
            QfirstSgBox.setText(targetVerb.get_indicativeFirstSg())
            QsecondSgBox.setText(targetVerb.get_indicativeSecondSg())
            QthirdSgBox.setText(targetVerb.get_indicativeThirdSg())
            QfirstPlBox.setText(targetVerb.get_indicativeFirstPl())
            QsecondPlBox.setText(targetVerb.get_indicativeSecondPl())
            QthirdPlBox.setText(targetVerb.get_indicativeThirdPl())
            QimperativeSgBox.setText(targetVerb.get_imperativeSg())
            QimperativePlBox.setText(targetVerb.get_imperativePl())
            QpastMascBox.setText(targetVerb.get_pastMasc())
            QpastFemBox.setText(targetVerb.get_pastFem())
            QpastNeutBox.setText(targetVerb.get_pastNeut())
            QpastPlBox.setText(targetVerb.get_pastPl())
            QdateDisplay.setText(targetVerb.get_nextStudyDateDisplay(user))




    def addVerbToCustom():
        target = QcustomQuizList.findItems(QverbList.currentItem().text(), QtCore.Qt.MatchExactly)
        if target == []:
            QcustomQuizList.addItem(QverbList.currentItem().text())

    def removeVerbFromCustom():
        rownum = QcustomQuizList.currentRow()
        QcustomQuizList.takeItem(rownum)

    def playConjugationAudio():
        verbAudio = './verbs/' + QverbList.currentItem().text() + '.mp3'
        playsound(verbAudio)

    QplayAudioButton.clicked.connect(playConjugationAudio)
    populateVerb(QverbList.currentItem().text()) #populate the conjugation for the verb in the first row
    QverbList.currentItemChanged.connect(lambda: populateVerb(QverbList.currentItem().text())) # any time a new row is selected, populate the conjugation for that row
    QaddToListBtn.clicked.connect(addVerbToCustom)
    QremoveFromListBtn.clicked.connect(removeVerbFromCustom)

    sys.exit(app.exec_())

def changeUserMsgBox(parent, userList):
    """create a dialog box which displays exising users and allows users to be added"""
    user, selectUser = QtGui.QInputDialog.getItem(parent,"Choose a User","Select a user or enter a new user:",userList)
    if selectUser and user != "":
        return user
    while (not selectUser) or (user == ""):
        user, selectUser = QtGui.QInputDialog.getItem(parent,"Choose a User","Select a user or enter a new user:",userList)
        if selectUser and user != "":
            return user



def getSortedVerbList(user):
    """returns a list of available verbs for the given user; verbs which have previously been studied are sorted at the front of the list by days overdue;
    other verbs are sorted by frequency rank"""
    with shelve.open('./verbs/verbsDB') as verbShelf:
        previouslyStudiedList = []
        notPreviouslyStudiedList = []
        for key in verbShelf:
            if key != 'users':
                print(key)
                print(verbShelf[key])
                if verbShelf[key].was_previouslyStudied(user):
                    previouslyStudiedList.append(key)
                else:
                    notPreviouslyStudiedList.append(key)
        previouslyStudiedList.sort(key=lambda x: verbShelf[x].get_daysOverdue(user), reverse=True)
        notPreviouslyStudiedList.sort(key=lambda x: verbShelf[x].get_conjugationAudio())
    return previouslyStudiedList + notPreviouslyStudiedList






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
