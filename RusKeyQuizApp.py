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



class mainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(mainWindow,self).__init__()
        self.QverbBrowser = QtGui.QWidget()
        with shelve.open('./verbs/verbsDB') as verbShelf:
            print(verbShelf['users'])
            self.user = self.changeUserMsgBox(self.QverbBrowser, verbShelf['users']) #creates a dialog box for choosing a user
            if self.user not in verbShelf['users']:
                temp = []
                for u in verbShelf['users']:
                    temp.append(u)
                temp.append(self.user)
                verbShelf['users'] = temp #add user to users item in verbShelf (store user permanently if not already stored)
        self.setGeometry(100,100,800,800)
        self.QmainMenu = self.menuBar()
        self.QfileMenu = self.QmainMenu.addMenu("File")
        self.QfileMenuAbout = QtGui.QAction("About", self.QmainMenu)
        self.QfileMenu.addAction(self.QfileMenuAbout)

        self.QfileMenuAbout.triggered.connect(self.aboutAction)
        self.QfileMenuManageUsers = QtGui.QAction("Manage Users", self.QmainMenu)
        self.QfileMenu.addAction(self.QfileMenuManageUsers)
        self.QfileMenuManageUsers.triggered.connect(self.manageUsers)
        self.QfileMenuQuit = QtGui.QAction("Quit", self.QmainMenu)
        self.QfileMenu.addAction(self.QfileMenuQuit)
        self.QfileMenuQuit.setShortcut("Ctrl+Q")
        self.QfileMenuQuit.triggered.connect(self.closeApp)


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
        self.QverbBrowserGrid = QtGui.QGridLayout() #main layout
        # ---------------------------------------------
        # NON PAST FORMS AREA
        #----------------------------------------------
        #    ___________
        #   |*NP***|    |     NP - non-past indicative forms - QNPISubGrid
        #   |______|____|
        #   |   |    |  |
        #   |___|____|__|
        #
        self.QNPISubGrid = QtGui.QGridLayout()
        self.QverbBrowserGrid.addLayout(self.QNPISubGrid, 0, 0, 1, 2)
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
        self.QinfoSubGrid = QtGui.QGridLayout()
        self.QNPIFormsSubGrid = QtGui.QGridLayout()
        self.QNPISubGrid.addLayout(self.QinfoSubGrid,0,0,2,1)
        self.QNPISubGrid.addLayout(self.QNPIFormsSubGrid,3,0,1,1)

        #----------------------------------------------
        # NON PAST INDICATIVE AREA LABEL:
        #----------------------------------------------
        self.QnonPastPaneLabel = QtSectionLabel("Non-Past Indicative Forms")
        self.QinfoSubGrid.addWidget(self.QnonPastPaneLabel,0,0,1,4)
        # ----------------------------------------------
        # PLAY AUDIO BUTTON:
        #-----------------------------------------------
        self.QplayAudioButton = QtGui.QPushButton("Play Audio")
        self.QinfoSubGrid.addWidget(self.QplayAudioButton,1,2,1,2)
        #-----------------------------------------------
        # INFINITIVE LABEL AND BOX
        #-----------------------------------------------
        self.QinfinitiveLabel = QtVFixedLabel("Infinitive:")
        self.QinfinitiveBox = QtDisplay()
        self.QinfoSubGrid.addWidget(self.QinfinitiveLabel,1,0,1,1)
        self.QinfoSubGrid.addWidget(self.QinfinitiveBox,1,1,1,1)

        #-----------------------------------------------
        # MEANING LABEL AND BOX
        #-----------------------------------------------
        self.QmeaningLabel = QtVFixedLabel("Meaning:")
        self.QmeaningBox = QtDisplayLong()
        self.QinfoSubGrid.addWidget(self.QmeaningLabel,2,0,1,1)
        self.QinfoSubGrid.addWidget(self.QmeaningBox,2,1,1,3)

        #-----------------------------------------------
        # ASPECT LABEL AND BOX
        #-----------------------------------------------
        self.QaspectLabel = QtVFixedLabel("Aspect:")
        self.QaspectBox = QtDisplay()
        self.QinfoSubGrid.addWidget(self.QaspectLabel,3,0,1,1)
        self.QinfoSubGrid.addWidget(self.QaspectBox,3,1,1,1)
        #-----------------------------------------------
        # FEQUENCY LABEL AND BOX
        #-----------------------------------------------
        self.QfrequencyLabel = QtVFixedLabel("Frequency Number:")
        self.QfrequencyBox = QtDisplay()
        self.QinfoSubGrid.addWidget(self.QfrequencyLabel,3,2,1,1)
        self.QinfoSubGrid.addWidget(self.QfrequencyBox,3,3,1,1)
        #-----------------------------------------------
        # 1ST PERSON SINGULAR INDICATIVE
        #-----------------------------------------------
        self.QfirstSgLabel = QtVFixedLabel("1st Person Singular:")
        self.QfirstSgBox = QtDisplay()
        self.QNPIFormsSubGrid.addWidget(self.QfirstSgLabel,0,0,1,1)
        self.QNPIFormsSubGrid.addWidget(self.QfirstSgBox,1,0,1,1)
        #-----------------------------------------------
        # 2ND PERSON SINGULAR INDICATIVE
        #-----------------------------------------------
        self.QsecondSgLabel = QtVFixedLabel("2nd Person Singular:")
        self.QsecondSgBox = QtDisplay()
        self.QNPIFormsSubGrid.addWidget(self.QsecondSgLabel,2,0,1,1)
        self.QNPIFormsSubGrid.addWidget(self.QsecondSgBox,3,0,1,1)
        #-----------------------------------------------
        # 3RD PERSON SINGULAR INDICATIVE
        #-----------------------------------------------
        self.QthirdSgLabel = QtVFixedLabel("3rd Person Singular:")
        self.QthirdSgBox = QtDisplay()
        self.QNPIFormsSubGrid.addWidget(self.QthirdSgLabel,4,0,1,1)
        self.QNPIFormsSubGrid.addWidget(self.QthirdSgBox,5,0,1,1)
        #-----------------------------------------------
        # 1ST PERSON PLURAL INDICATIVE
        #-----------------------------------------------
        self.QfirstPlLabel = QtVFixedLabel("1st Person Plural:")
        self.QfirstPlBox = QtDisplay()
        self.QNPIFormsSubGrid.addWidget(self.QfirstPlLabel,0,2,1,1)
        self.QNPIFormsSubGrid.addWidget(self.QfirstPlBox,1,2,1,1)
        #-----------------------------------------------
        # 2ND PERSON PLURAL INDICATIVE
        #-----------------------------------------------
        self.QsecondPlLabel = QtVFixedLabel("2nd Person Plural:")
        self.QsecondPlBox = QtDisplay()
        self.QNPIFormsSubGrid.addWidget(self.QsecondPlLabel,2,2,1,1)
        self.QNPIFormsSubGrid.addWidget(self.QsecondPlBox,3,2,1,1)
        #-----------------------------------------------
        # 3rd PERSON PLURAL INDICATIVE
        #-----------------------------------------------
        self.QthirdPlLabel = QtVFixedLabel("3rd Person Plural:")
        self.QthirdPlBox = QtDisplay()
        self.QNPIFormsSubGrid.addWidget(self.QthirdPlLabel,4,2,1,1)
        self.QNPIFormsSubGrid.addWidget(self.QthirdPlBox,5,2,1,1)




        # ---------------------------------------------
        # PAST AND IMPERATIVE FORMS AREA
        #----------------------------------------------
        #    ___________
        #   |      |P&I*|     P&I - Past and Imperative Forms - QPastSubGrid
        #   |______|____|
        #   |   |    |  |
        #   |___|____|__|
        #
        self.QPastSubGrid = QtGui.QGridLayout()
        self.QverbBrowserGrid.addLayout(self.QPastSubGrid,0,2,1,1)
    #
    #
    #
        #----------------------------------------------
        # PAST AND IMPERATIVE AREA LABEL:
        #----------------------------------------------
        self.QPastPaneLabel = QtSectionLabel("Imperative and Past Forms")
        self.QPastSubGrid.addWidget(self.QPastPaneLabel,0,0,1,2)
        #-----------------------------------------------
        # IMPERATIVE SINGULAR
        #-----------------------------------------------
        self.QimperativeSgLabel = QtVFixedLabel("Imperative Singular:")
        self.QimperativeSgBox = QtDisplay()
        self.QPastSubGrid.addWidget(self.QimperativeSgLabel,1,0,1,1)
        self.QPastSubGrid.addWidget(self.QimperativeSgBox,1,1,1,1)
        #-----------------------------------------------
        # IMPERATIVE PLURAL
        #-----------------------------------------------
        self.QimperativePlLabel = QtVFixedLabel("Imperative Plural:")
        self.QimperativePlBox = QtDisplay()
        self.QPastSubGrid.addWidget(self.QimperativePlLabel,2,0,1,1)
        self.QPastSubGrid.addWidget(self.QimperativePlBox,2,1,1,1)
        #-----------------------------------------------
        # PAST MASCULINE
        #-----------------------------------------------
        self.QpastMascLabel = QtVFixedLabel("Past Masculine:")
        self.QpastMascBox = QtDisplay()
        self.QPastSubGrid.addWidget(self.QpastMascLabel,3,0,1,1)
        self.QPastSubGrid.addWidget(self.QpastMascBox,3,1,1,1)
        #-----------------------------------------------
        # PAST FEMININE
        #-----------------------------------------------
        self.QpastFemLabel = QtVFixedLabel("Past Feminine:")
        self.QpastFemBox = QtDisplay()
        self.QPastSubGrid.addWidget(self.QpastFemLabel,4,0,1,1)
        self.QPastSubGrid.addWidget(self.QpastFemBox,4,1,1,1)
        #-----------------------------------------------
        # PAST NEUTER
        #-----------------------------------------------
        self.QpastNeutLabel = QtVFixedLabel("Past Neuter:")
        self.QpastNeutBox = QtDisplay()
        self.QPastSubGrid.addWidget(self.QpastNeutLabel,5,0,1,1)
        self.QPastSubGrid.addWidget(self.QpastNeutBox,5,1,1,1)
        #-----------------------------------------------
        # PAST PLURAL
        #-----------------------------------------------
        self.QpastPlLabel = QtVFixedLabel("Past Plural:")
        self.QpastPlBox = QtDisplay()
        self.QPastSubGrid.addWidget(self.QpastPlLabel,6,0,1,1)
        self.QPastSubGrid.addWidget(self.QpastPlBox,6,1,1,1)

        #-----------------------------------------------
        # DYNAMICALLY ALLOCATED SPACE FOR EXAMPLES - this holder will be populated by a displayVerb function, since the number of examples
        # varies from verb to verb
        #-----------------------------------------------
        self.QexamplesGrid = QtGui.QGridLayout()
        self.QverbBrowserGrid.addLayout(self.QexamplesGrid,1,0,1,3)

        #-----------------------------------------------
        # BOTTOM SECIONS
        #-----------------------------------------------
        #    ___________
        #   |      |    |     QbottomGrid - houses the three subdivisions of the bottom sections
        #   |______|____|
        #   |***********|
        #   |___________|
        #
        self.QbottomGrid = QtGui.QGridLayout()
        self.QverbBrowserGrid.addLayout(self.QbottomGrid,2,0,1,3)
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
        self.QverbListGrid = QtGui.QGridLayout()
        self.QbottomGrid.addLayout(self.QverbListGrid,0,0,1,1)
        self.QverbListLabel = QtSectionLabel("Browse Available Verbs")
        self.QverbList = QtGui.QListWidget()
        #----------------------------------------------
        # DATE STUDIED DISPLAY
        #----------------------------------------------
        self.QdateLabel = QtVFixedLabel('Due date:')
        self.QdateDisplay = QtDisplay()
        self.QverbListGrid.addWidget(self.QdateLabel,0,0,1,1)
        self.QverbListGrid.addWidget(self.QdateDisplay,0,1,1,1)
        self.QverbListGrid.addWidget(self.QverbListLabel,1,0,1,2)
        self.QverbListGrid.addWidget(self.QverbList,2,0,1,2)
        #------------------------------------------------
        #    ___________
        #   |      |    |
        #   |______|____|
        #   |   | btn|  |
        #   |___|____|__|     btn - buttons to add verbs to quiz
        #
        #------------------------------------------------
        self.QbuttonAreaGrid = QtGui.QGridLayout()
        self.QbottomGrid.addLayout(self.QbuttonAreaGrid,0,1,1,1)
        self.QchangeUserBtn = QtGui.QPushButton("Change User")
        self.QautoQuizBtn = QtGui.QPushButton("Quiz on Most Overdue Items (auto)")
        self.QcustomQuizBtn = QtGui.QPushButton("Quiz on Custom List -->")
        self.QaddToListBtn = QtGui.QPushButton("-- Add to Quiz List -->")
        self.QremoveFromListBtn = QtGui.QPushButton("<-- Remove from Quiz List --")
        self.QbuttonAreaGrid.addWidget(self.QchangeUserBtn,0,0,1,1)
        self.QbuttonAreaGrid.addWidget(self.QautoQuizBtn,1,0,1,1)
        self.QbuttonAreaGrid.addWidget(self.QcustomQuizBtn,2,0,1,1)
        self.QbuttonAreaGrid.addWidget(self.QaddToListBtn,3,0,1,1)
        self.QbuttonAreaGrid.addWidget(self.QremoveFromListBtn,4,0,1,1)
        #-------------------------------------------------
        #    ___________
        #   |      |    |
        #   |______|____|
        #   |   |    | q|
        #   |___|____|__|
        #                     q - list of verbs selected for custom quiz
        #-------------------------------------------------
        self.QcustomQuizGrid = QtGui.QGridLayout()
        self.QbottomGrid.addLayout(self.QcustomQuizGrid,0,2,1,1)
        self.QcustomQuizLabel = QtSectionLabel("Custom Quiz List")
        self.QcustomQuizList = QtGui.QListWidget()
        #----------------------------------------------
        # CURRENT USER DISPLAY
        #----------------------------------------------
        self.QuserLabel = QtVFixedLabel('Current User:')
        self.QuserBox = QtDisplay()
        self.QcustomQuizGrid.addWidget(self.QuserLabel,0,0,1,1)
        self.QcustomQuizGrid.addWidget(self.QuserBox,0,1,1,1)
        self.QcustomQuizGrid.addWidget(self.QcustomQuizLabel,1,0,1,2)
        self.QcustomQuizGrid.addWidget(self.QcustomQuizList,2,0,1,2)

        self.QverbBrowser.setLayout(self.QverbBrowserGrid)
        self.setWindowTitle("RusKey Verb Browser")
        self.setCentralWidget(self.QverbBrowser)
        self.QuserBox.setText(self.user)
        self.verbs = self.getSortedVerbList(self.user) #load the verb list in the relevant due date order for user
        self.QverbList.addItems(self.verbs) #add the verbs in order to the QListWidget
        self.QverbList.setCurrentRow(0) #select the first row by default
        self.QplayAudioButton.clicked.connect(self.playConjugationAudio)
        self.populateVerb(self.QverbList.currentItem().text()) #populate the conjugation for the verb in the first row
        self.QverbList.currentItemChanged.connect(lambda: self.populateVerb(self.QverbList.currentItem().text())) # any time a new row is selected, populate the conjugation for that row
        self.QaddToListBtn.clicked.connect(self.addVerbToCustom)
        self.QremoveFromListBtn.clicked.connect(self.removeVerbFromCustom)

    def populateVerb(self, verbKey): #function to update conjugation display when new verb in QverbList is selected
        with shelve.open('./verbs/verbsDB') as verbShelf:
            targetVerb = verbShelf[verbKey]
            self.QinfinitiveBox.setText(targetVerb.get_infinitive())
            self.QmeaningBox.setText(targetVerb.get_meaning())
            self.QaspectBox.setText(targetVerb.get_aspect())
            self.QfrequencyBox.setText(targetVerb.get_frequencyRank())
            self.QfirstSgBox.setText(targetVerb.get_indicativeFirstSg())
            self.QsecondSgBox.setText(targetVerb.get_indicativeSecondSg())
            self.QthirdSgBox.setText(targetVerb.get_indicativeThirdSg())
            self.QfirstPlBox.setText(targetVerb.get_indicativeFirstPl())
            self.QsecondPlBox.setText(targetVerb.get_indicativeSecondPl())
            self.QthirdPlBox.setText(targetVerb.get_indicativeThirdPl())
            self.QimperativeSgBox.setText(targetVerb.get_imperativeSg())
            self.QimperativePlBox.setText(targetVerb.get_imperativePl())
            self.QpastMascBox.setText(targetVerb.get_pastMasc())
            self.QpastFemBox.setText(targetVerb.get_pastFem())
            self.QpastNeutBox.setText(targetVerb.get_pastNeut())
            self.QpastPlBox.setText(targetVerb.get_pastPl())
            self.QdateDisplay.setText(targetVerb.get_nextStudyDateDisplay(self.user))

    def aboutAction(self):
        self.QaboutWindow = QtGui.QMessageBox(self)
        self.QaboutWindow.setGeometry(150,150,300,300)
        self.QaboutWindow.setText("RusKey is an opensource project developed by Eli Ginsburg-Marcy. The examples, conjugations, and frequency rankings it contains are derived from data scraped from en.openrussian.org")
        self.QaboutWindow.setWindowTitle("About RusKey")
        self.QaboutWindow.setIcon(QtGui.QMessageBox.Information)
        self.QaboutWindow.setStandardButtons(QtGui.QMessageBox.Close)
        self.QaboutWindow.exec_()

    def getUserList(self):
        """returns a list of users stored in verbDB['users']"""
        with shelve.open('./verbs/verbsDB') as verbShelf:
            userList = []
            for u in verbShelf['users']:
                userList.append(u)
            userList.sort()
        return userList

    def manageUsers(self):
        QmanageUsersWindow = QtGui.QDialog(self)
        QmanageUsersWindow.setWindowFlags(QtCore.Qt.Window)
        QmanageUsersWindow.setGeometry(150,150,400,400)
        QmanageUsersGrid = QtGui.QGridLayout()
        QuserDispLabelMgUsers = QtVFixedLabel("Current User:")
        QuserDisplayMgUsers = QtDisplay()
        QuserDisplayMgUsers.setText(self.user)
        QchangeUserBtnMgUsers = QtGui.QPushButton("Change to Selected User")
        QdeleteUserBtn = QtGui.QPushButton("Delete Selected User")
        QuserList = QtGui.QListWidget()
        QuserList.addItems(self.getUserList())
        QmanageUsersGrid.addWidget(QuserDispLabelMgUsers,0,0,1,1)
        QmanageUsersGrid.addWidget(QuserDisplayMgUsers,0,1,1,1)
        QmanageUsersGrid.addWidget(QchangeUserBtnMgUsers,1,0,1,2)
        QmanageUsersGrid.addWidget(QdeleteUserBtn,2,0,1,2)
        QmanageUsersGrid.addWidget(QuserList,3,0,1,2)
        QmanageUsersWindow.setLayout(QmanageUsersGrid)
        QmanageUsersWindow.setWindowTitle("Manage Users")

        QuserList.setCurrentRow(0)
        def verifyChangeUserBox():
            """verification window for changing users"""
            Qverify = QtGui.QMessageBox(QmanageUsersWindow)
            Qverify.setText("Are you sure you wish to change users?")
            Qverify.setIcon(QtGui.QMessageBox.Warning)
            Qverify.setStandardButtons(QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if QuserList.currentItem().text() != self.user:
                result = Qverify.exec_()
                if result == QtGui.QMessageBox.Yes:
                    self.user = QuserList.currentItem().text()
                    QuserDisplayMgUsers.setText(self.user)
                    self.QuserBox.setText(self.user)
                    self.QverbList.clear()
                    self.verbs = self.getSortedVerbList(self.user) #load the verb list in the relevant due date order for user
                    self.QverbList.addItems(self.verbs) #add the verbs in order to the QListWidget
        def deleteUser():
            """verification window for deleting a user"""
            if QuserList.currentItem().text() == self.user:
                Qnotice = QtGui.QMessageBox(QmanageUsersWindow)
                Qnotice.setText("Cannot delete the current user!")
                Qnotice.setIcon(QtGui.QMessageBox.Information)
                Qnotice.setStandardButtons(QtGui.QMessageBox.Ok)
                Qnotice.exec_()
            else:
                Qverify = QtGui.QMessageBox(QmanageUsersWindow)
                Qverify.setText("Are you sure you wish to DELETE the given user? This operation cannot be undone.")
                Qverify.setIcon(QtGui.QMessageBox.Warning)
                Qverify.setStandardButtons(QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
                result = Qverify.exec_()
                if result == QtGui.QMessageBox.Yes:
                    userList = self.getUserList()
                    userList.remove(QuserList.currentItem().text())
                    with shelve.open('./verbs/verbsDB') as verbShelf:
                        verbShelf['users'] = userList
                    QuserList.clear()
                    QuserList.addItems(self.getUserList())


        QdeleteUserBtn.clicked.connect(deleteUser)
        QchangeUserBtnMgUsers.clicked.connect(verifyChangeUserBox)
        QmanageUsersWindow.exec_()

    def addVerbToCustom(self):
        target = self.QcustomQuizList.findItems(self.QverbList.currentItem().text(), QtCore.Qt.MatchExactly)
        if target == []:
            self.QcustomQuizList.addItem(self.QverbList.currentItem().text())

    def removeVerbFromCustom(self):
        rownum = self.QcustomQuizList.currentRow()
        self.QcustomQuizList.takeItem(rownum)

    def playConjugationAudio(self):
        verbAudio = './verbs/' + self.QverbList.currentItem().text() + '.mp3'
        playsound(verbAudio)



    def changeUserMsgBox(self, parent, userList):
        """create a dialog box which displays exising users and allows users to be added"""
        user, selectUser = QtGui.QInputDialog.getItem(parent,"Choose a User","Select a user or enter a new user:",userList)
        if selectUser and user != "":
            return user
        while (not selectUser) or (user == ""):
            user, selectUser = QtGui.QInputDialog.getItem(parent,"Choose a User","Select a user or enter a new user:",userList)
            if selectUser and user != "":
                return user


    def closeApp(self):
        sys.exit()

    def test():
        print("It worked!")



    def getSortedVerbList(self, user):
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

    app =  QtGui.QApplication(sys.argv)
    w = mainWindow()
    w.show()
    sys.exit(app.exec_())
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
