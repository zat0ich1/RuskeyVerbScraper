#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 10:27:24 2017

@author: eli
"""

import os
import shelve
import datetime
import random
from PyQt4 import QtCore


class verb(object):
    def __init__(self, verbFileName):
        with open('./verbs/'+verbFileName) as verbFile:
            self.verbFileLinesList = verbFile.readlines()
            self.infinitive = self.verbFileLinesList[0].replace(u'\n','')
            self.aspect = self.verbFileLinesList[1].replace(u'\n','')
            self.frequencyRank = self.verbFileLinesList[2].replace(u'\n','')
            self.meaning = self.verbFileLinesList[3].replace(u'\n','')
            self.indicativeFirstSg = self.verbFileLinesList[4].replace(u'\n','')
            self.indicativeSecondSg = self.verbFileLinesList[5].replace(u'\n','')
            self.indicativeThirdSg = self.verbFileLinesList[6].replace(u'\n','')
            self.indicativeFirstPl = self.verbFileLinesList[7].replace(u'\n','')
            self.indicativeSecondPl = self.verbFileLinesList[8].replace(u'\n','')
            self.indicativeThirdPl = self.verbFileLinesList[9].replace(u'\n','')
            self.imperativeSg = self.verbFileLinesList[10].replace(u'\n','')
            self.imperativePl = self.verbFileLinesList[11].replace(u'\n','')
            self.pastMasc = self.verbFileLinesList[12].replace(u'\n','')
            self.pastFem = self.verbFileLinesList[13].replace(u'\n','')
            self.pastNeut = self.verbFileLinesList[14].replace(u'\n','')
            self.pastPl = self.verbFileLinesList[15].replace(u'\n','')
            self.examplesList = []
            self.examplesListTranslations = []
            self.verbAudioList = []
            for i in range(16,len(self.verbFileLinesList)-1,2):
                self.examplesList.append(self.verbFileLinesList[i].replace(u'\n',''))
                self.examplesListTranslations.append(self.verbFileLinesList[i+1].replace(u'\n',''))
            for i in range(len(self.examplesList)):
                audioFileName = './verbs/' + verbFileName[:-4] + str(i) + '.mp3'
                self.verbAudioList.append(audioFileName)
            self.verbAudioList.append('./verbs/'+verbFileName[:-4]+'.mp3') #append conjugation audio last so that indexes for examples line up
            self.easinessFactor = {} # these dictionaries will be used with SM2 algorithm to
            self.lastInterval = {}     # find out when the object should next be studied; keys are user names
            self.dateLastStudied = {} # will be updated when first studied
            self.previouslyStudied = {}
            self.dueDate = {}

    def __str__(self):
        string = 'infinitive: {:>20}'.format(self.infinitive) + '\n' + \
        'frequency: {:>20}'.format(self.frequencyRank) + '\n' + \
        'meaning: {:>20}'.format(self.meaning) + '\n' + \
        'aspect: {:>20}'.format(self.aspect) + '\n' + \
        'indicative 1st sg: {:>20}'.format(self.indicativeFirstSg) + '\n' + \
        'indicative 2nd sg: {:>20}'.format(self.indicativeSecondSg) + '\n' + \
        'indicative 3rd sg: {:>20}'.format(self.indicativeThirdSg) + '\n' + \
        'indicative 1st pl: {:>20}'.format(self.indicativeFirstPl) + '\n' + \
        'indicative 2nd pl: {:>20}'.format(self.indicativeSecondPl) + '\n' + \
        'indicative 3rd pl: {:>20}'.format(self.indicativeThirdPl) + '\n' + \
        'imperative sg: {:>20}'.format(self.imperativeSg) + '\n' + \
        'imperative pl: {:>20}'.format(self.imperativePl) + '\n' + \
        'past masc: {:>20}'.format(self.pastMasc) + '\n' + \
        'past fem: {:>20}'.format(self.pastFem) + '\n' + \
        'past neut: {:>20}'.format(self.pastNeut) + '\n' + \
        'past pl: {:>20}'.format(self.pastPl) + '\n'
        for i in range(len(self.examplesList)):
            if i != len(self.examplesList):
                string += 'example '+str(i)+': {:>50}'.format(self.examplesList[i]) + '\n' + \
                'translation: {:>50}'.format(self.examplesListTranslations[i]) + '\n' + \
                'audio file: {:>50}'.format(self.verbAudioList[i]) + '\n'
        string += 'conjugation audio file: {:>40}'.format(self.verbAudioList[len(self.verbAudioList)-1])
        return string

    def get_infinitive(self):
        """returns a string of the infinitive form of the verb"""
        return self.infinitive
    def get_aspect(self):
        """returns a string representing the aspect of the verb"""
        return self.aspect
    def get_frequencyRank(self):
        """returns a string representing the frequency number for the verb"""
        return self.frequencyRank
    def get_meaning(self):
        """returns a string containing common translations of the verb"""
        return self.meaning
    def get_indicativeFirstSg(self):
        """returns a string containing the non-past indicative 1st person singular form of the verb"""
        return self.indicativeFirstSg
    def get_indicativeSecondSg(self):
        """returns a string containing the non-past indicative 2nd person singular form of the verb"""
        return self.indicativeSecondSg
    def get_indicativeThirdSg(self):
        """returns a string containing the non-past indicative 3rd person singular form of the verb"""
        return self.indicativeThirdSg
    def get_indicativeFirstPl(self):
        """returns a string containing the non-past indicative 1st person plural form of the verb"""
        return self.indicativeFirstPl
    def get_indicativeSecondPl(self):
        """returns a string containing the non-past indicative 2nd person plural form of the verb"""
        return self.indicativeSecondPl
    def get_indicativeThirdPl(self):
        """returns a string containing the non-past indicative 3rd person plural form of the verb"""
        return self.indicativeThirdPl
    def get_imperativeSg(self):
        """returns a string containing the imperative singular form of the verb"""
        return self.imperativeSg
    def get_imperativePl(self):
        """returns a string containing the imperative plural form of the verb"""
        return self.imperativePl
    def get_pastMasc(self):
        """returns a string containing the past masculine form of the verb"""
        return self.pastMasc
    def get_pastFem(self):
        """returns a string containing the past feminine form of the verb"""
        return self.pastFem
    def get_pastNeut(self):
        """returns a string containing the past neuter form of the verb"""
        return self.pastNeut
    def get_pastPl(self):
        """returns a string containing the past plural form of the verb"""
        return self.pastPl
    def get_examplesList(self, stripPunctuation=False):
        """takes an optional parameter to strip punctuation marks; returns a list of the russian example sentences; the indices for these match the indices in the corresponding translation list"""
        if not stripPunctuation:
            return self.examplesList
        else:
            strippedList = []
            for string in self.examplesList[:]:
                string = string.replace(',','')
                string = string.replace('.','')
                string = string.replace(':','')
                string = string.replace(';','')
                string = string.replace('?','')
                string = string.replace('!','')
                strippedList.append(string)
            return strippedList
    def get_examplesListTranslations(self):
        """returns a list of translations of the russian example sentences; the indices for these match the indices in the corresponding examples list"""
        return self.examplesListTranslations
    def get_verbAudioList(self):
        """returns a list of the audio file names for the verb. The indices should match the example sentence list indices, excepting the final item, which is the audio for the conjugation"""
        return self.verbAudioList
    def get_conjugationAudio(self):
        """returns the name of the conjugation audio file"""
        return self.verbAudioList[-1]
    def get_randomizedExamplesList(self):
        """returns a list of randomized example sentences; each member of the list is a list of the words in the example in random order\n
        e.g. the example sentence 'Я была с ним честной' becomes ['Я', 'с', 'была', 'ним', 'честной'] (this list would be a member of the list returned)"""
        randomizedExamples = []
        for string in self.examplesList:
            string = string.replace(',','')
            string = string.replace('.','')
            string = string.replace(':','')
            string = string.replace(';','')
            string = string.replace('?','')
            string = string.replace('!','')
            sentenceList = string.split(' ')
            random.shuffle(sentenceList)
            randomizedExamples.append(sentenceList)
        return randomizedExamples
    def addUser(self, user):
        """adds a user to the dictionaries used for the spaced repetition algorithm and preloads default values in these dictionaries"""
        self.easinessFactor[user] = 2.5
        self.lastInterval[user] = 1
        self.previouslyStudied [user] = False
        self.dateLastStudied[user] = QtCore.QDate.currentDate()
        self.dueDate[user] = self.dateLastStudied[user].addDays(self.lastInterval[user])
    def was_previouslyStudied(self, user):
        """returns the value of self.previouslyStudied for the user specified; used to determine whether a user should be presented with familiarization
        screens prior to quiz initiation"""
        return self.previouslyStudied[user]
    def update_study_interval(self, user, score):
        """user - a string of the name of the user whose interval is to be updated; score - a number between 0 and 1 representing performance on quiz;
        updates the desired study interval for the user (self.easinessFactor and self.lastInterval) using the SM2 algorithm"""
        self.previouslyStudied[user] = True
        self.set_dateLastStudied(user)
        if (score*5) < 3.5:
            self.lastInterval[user] = 1
        else:
            if self.lastInterval.get(user, 1) == 1:
                self.lastInterval[user] = 2
            elif self.lastInterval[user] == 2:
                self.lastInterval[user] = 4
            else:
                self.easinessFactor[user] += (0.1-(5-(score*5))*(0.08+(5-(score*5))*0.02))
                if self.easinessFactor[user] < 1.3:
                    self.easinessFactor[user] = 1.3
                elif self.easinessFactor[user] > 5:
                    self.easinessFactor[user] = 5
                self.lastInterval[user] *= self.easinessFactor[user]
                self.lastInterval[user] = int(self.lastInterval[user])
        self.dueDate[user] = self.dateLastStudied[user].addDays(self.lastInterval[user])
    def set_dateLastStudied(self, user, date=QtCore.QDate.currentDate()):
        """user - the user whose date last studied you want to set; date - QDate object - defaults to current date;
        updates dateLastStudied for the specified user to the specified date"""
        self.dateLastStudied[user] = date
    def get_dateLastStudied(self, user):
        """user - the user whose dateLastStudied you wish to retrieve; returns a QDate object for the date last studied"""
        return self.dateLastStudied.get(user, QtCore.QDate.currentDate())
    def get_nextStudyDate(self,user):
        """returns the date on which the user should next study a verb according to the SM2 algorithm;
        if this date is before the current date, returns the phrase "Overdue"; if the user has not yet studied a verb
        returns the phrase 'Not yet studied'"""
        if not self.was_previouslyStudied(user):
            return "Not yet studied"
        else:
            if self.is_overdue(user):
                return "Overdue"
            else:
                displayDate = self.dueDate[user]
                displayDate.toString('MM dd yyyy')
                if displayDate == QtCore.QDate.currentDate():
                    return("Due today!")
                return displayDate.toString('MM/dd/yyyy')
    def is_overdue(self, user):
        """returns True if a verb is overdue; False otherwise"""
        if not self.was_previouslyStudied(user):
            return False
        elif self.get_daysOverdue(user) > 0:
            return True
        else:
            return False
    def get_daysOverdue(self,user):
        """returns the difference between today's date and the next study date"""
        return self.dueDate[user].daysTo(QtCore.QDate.currentDate())
    def get_dueDate(self,user):
        """returns a the due date for a verb for the given user (a QDate object)"""
        return self.dueDate[user]
    def set_dueDate(self,user):
        self.dueDate[user] = self.dateLastStudied[user].addDays(self.lastInterval[user])

#testing -----
delimiter = '=========================================='
byt = verb('0001byt.txt')
skazat = verb('0002skazat.txt')
print(delimiter)
print('PRINT ENTIRE CONJUGATION INFO FOR BYT')
print(byt)
print(delimiter)
print('PRINT ENTIRE CONJUGATION INFO FOR SKAZAT')
print(skazat)
print(delimiter)
print("INFINITIVE GETTER; BYT THEN SKAZAT")
print(byt.get_infinitive())
print(skazat.get_infinitive())
print(delimiter)
print('ASPECT GETTER: BYT THEN SKAZAT')
print(byt.get_aspect())
print(skazat.get_aspect())
print(delimiter)
print('FREQUENCY GETTER; BYT THEN SKAZAT')
print(byt.get_frequencyRank())
print(skazat.get_frequencyRank())
print(delimiter)
print('MEANING GETTER; BYT THEN SKAZAT')
print(byt.get_meaning())
print(skazat.get_meaning())
print(delimiter)
print('INDICATIVE FIRST SINGULAR GETTER; BYT THEN SKAZAT')
print(byt.get_indicativeFirstSg())
print(skazat.get_indicativeFirstSg())
print(delimiter)
print('INDICATIVE SECOND PERSON SINGULAR; BYT THEN SKAZAT')
print(byt.get_indicativeSecondSg())
print(skazat.get_indicativeSecondSg())
print(delimiter)
print('INDICATIVE THIRD PERSON PLURAL; BYT THEN SKAZAT')
print(byt.get_indicativeThirdSg())
print(skazat.get_indicativeThirdSg())
print(delimiter)
print('INDICATIVE 1ST PERSON PLURAL: BYT THEN SKAZAT')
print(byt.get_indicativeFirstPl())
print(skazat.get_indicativeFirstPl())
print(delimiter)
print('INDICATIVE 2ND PERSON PLURAL; BYT THEN SKAZAT')
print(byt.get_indicativeSecondPl())
print(skazat.get_indicativeSecondPl())
print(delimiter)
print('INDICATIVE 3RD PERSON PLURAL;BYT THEN SKAZAT')
print(byt.get_indicativeThirdPl())
print(skazat.get_indicativeThirdPl())
print(delimiter)
print('IMPERATIVE SINGULAR; BYT THEN SKAZAT')
print(byt.get_imperativeSg())
print(skazat.get_imperativeSg())
print(delimiter)
print('IMPERATIVE PLURAL; BYT THEN SKAZAT')
print(byt.get_imperativePl())
print(skazat.get_imperativePl())
print(delimiter)
print('PAST MASCULINE; BYT THEN SKAZAT')
print(byt.get_pastMasc())
print(skazat.get_pastMasc())
print(delimiter)
print('PAST FEMININE; BYT THEN SKAZAT')
print(byt.get_pastFem())
print(skazat.get_pastFem())
print(delimiter)
print('PAST NEUTER; BYT THEN SKAZAT')
print(byt.get_pastNeut())
print(skazat.get_pastNeut())
print(delimiter)
print('PAST PLURAL; BYT THEN SKAZAT')
print(byt.get_pastPl())
print(skazat.get_pastPl())
print(delimiter)
print('Examples List Functionality; Print each example, each example stripped of punctuation its translation, and then the file name for the corresponding audio; byt then skazat')
bytExList = byt.get_examplesList()
bytExListStripped = byt.get_examplesList(True)
bytTransList = byt.get_examplesListTranslations()
bytFileList = byt.get_verbAudioList()
skazatExList = skazat.get_examplesList()
skazatExListStripped = skazat.get_examplesList(True)
skazatTransList = skazat.get_examplesListTranslations()
skazatFileList = skazat.get_verbAudioList()
print(delimiter)
for i in range(len(bytExList)):
    print(bytExList[i])
    print(bytExListStripped[i])
    print(bytTransList[i])
    print(bytFileList[i])
    print(delimiter)
for i in range(len(skazatExList)):
    print(skazatExList[i])
    print(skazatExListStripped[i])
    print(skazatTransList[i])
    print(skazatFileList[i])
    print(delimiter)
print("CONJUGATION AUDIO FOR BYT AND SKAZAT")
print(byt.get_conjugationAudio())
print(skazat.get_conjugationAudio())
print(delimiter)
print("RANDOMIZED STRIPPED EXAMPLES; BYT AND SKAZAT")
bytRandomExList = byt.get_randomizedExamplesList()
skazatRandomExList = skazat.get_randomizedExamplesList()
for example in bytRandomExList:
    print(example)
print(delimiter)
for example in skazatRandomExList:
    print(example)
print(delimiter)
print("USER BASED TESTS - USERS TIM AND ANNA")
byt.addUser('Tim')
skazat.addUser('Tim')
byt.addUser('Anna')
skazat.addUser('Anna')
print("BEFORE STUDY; WAS PREVIOUSLY STUDIED SHOULD RETURN FALSE")
print("TIM (BYT):", byt.was_previouslyStudied('Tim'))
print("ANNA (BYT):", byt.was_previouslyStudied('Anna'))
print("TIM (SKAZAT):", skazat.was_previouslyStudied('Tim'))
print("ANNA (SKAZAT):", skazat.was_previouslyStudied('Anna'))
print("DUE DATE SHOULD BE INTIALIZED FOR THESE USERS TO ONE DAY FROM NOW")
print("TIM (BYT):", byt.get_dueDate('Tim'))
print("ANNA (BYT):", byt.get_dueDate('Anna'))
print("TIM (SKAZAT):", skazat.get_dueDate('Tim'))
print("ANNA (SKAZAT):", skazat.get_dueDate('Anna'))
print("TIM AND ANNA STUDY BYT AND SKAZAT AND SCORE 80")
byt.update_study_interval('Tim',0.8)
byt.update_study_interval('Anna',0.8)
skazat.update_study_interval('Tim',0.8)
skazat.update_study_interval('Anna',0.8)
print("WAS PREVIOUSLY STUDIED SHOULD NOW RETURN TRUE")
print("TIM (BYT):", byt.was_previouslyStudied('Tim'))
print("ANNA (BYT):", byt.was_previouslyStudied('Anna'))
print("TIM (SKAZAT):", skazat.was_previouslyStudied('Tim'))
print("ANNA (SKAZAT):", skazat.was_previouslyStudied('Anna'))
print("DUE DATE SHOULD BE UPDATED FROM PREVIOUS VALUE:")
print("TIM (BYT):", byt.get_dueDate('Tim'))
print("ANNA (BYT):", byt.get_dueDate('Anna'))
print("TIM (SKAZAT):", skazat.get_dueDate('Tim'))
print("ANNA (SKAZAT):", skazat.get_dueDate('Anna'))
print("IS OVERDUE SHOULD RETURN FALSE")
print("TIM (BYT):", byt.is_overdue('Tim'))
print("TIM (SKAZAT):", skazat.is_overdue('Tim'))
print("ANNA (BYT):",byt.is_overdue('Anna'))
print("ANNA (SKAZAT):",skazat.is_overdue('Anna'))
print("TESTING SETTING AND GETTING DATE; SET DATE LAST STUDIED TO 2 WEEKS AGO")
twoWeeksAgo = QtCore.QDate.currentDate()
twoWeeksAgo = twoWeeksAgo.addDays(-14)
byt.set_dateLastStudied('Tim',twoWeeksAgo)
byt.set_dateLastStudied('Anna',twoWeeksAgo)
skazat.set_dateLastStudied('Tim',twoWeeksAgo)
skazat.set_dateLastStudied('Anna',twoWeeksAgo)
byt.set_dueDate('Tim')
byt.set_dueDate('Anna')
skazat.set_dueDate('Tim')
skazat.set_dueDate('Anna')
print("TIM (BYT) - SHOULD RETURN TWO WEEKS AGO")
print(byt.get_dateLastStudied('Tim'))
print('TIM (SKAZAT) - SHOULD RETURN TWO WEEKS AGO')
print(skazat.get_dateLastStudied('Tim'))
print('ANNA (BYT) - SHOULD RETURN TWO WEEKS AGO')
print(byt.get_dateLastStudied('Anna'))
print('ANNA (SKAZAT) - SHOULD RETURN TWO WEEKS AGO')
print(skazat.get_dateLastStudied('Anna'))
print("BYT AND SKAZAT SHOULD BOTH BE OVERDUE NOW THAT THE DATE LAST STUDIED HAS BEEN SET TO TWO WEEKS AGO")
print("GET NEXT STUDY DATE FOR TIM (BYT) - SHOULD RETURN OVERDUE")
print(byt.get_nextStudyDate('Tim'))
print("GET NEXT STUDY DATE FOR TIM (SKAZAT) - SHOULD RETURN OVERDUE")
print(skazat.get_nextStudyDate('Tim'))
print("GET NEXT STUDY DATE FOR ANNA (BYT) - SHOULD RETURN OVERDUE")
print(byt.get_nextStudyDate('Anna'))
print("GET NEXT STUDY DATE FOR ANNA (SKAZAT) - SHOULD RETURN OVERDUE")
print(skazat.get_nextStudyDate('Anna'))
print("IS OVERDUE FUNCTION TIM (BYT) - SHOULD RETURN TRUE")
print(byt.is_overdue('Tim'))
print("IS OVERDUE FUNCTION TIM (SKAZAT) - SHOULD RETURN TRUE")
print(skazat.is_overdue('Tim'))
print("IS OVERDUE FUNCTION ANNA (BYT) - SHOULD RETURN TRUE")
print(byt.is_overdue('Anna'))
print("IS OVERDUE FUNCTION ANNA (SKAZAT) - SHOULD RETURN TRUE")
print(skazat.is_overdue('Anna'))
print("GET DAYS OVERDUE; SHOULD RETURN AN INT > 0")
print("TIM (BYT):",byt.get_daysOverdue('Tim'))
print("TIM (SKAZAT):",skazat.get_daysOverdue('Tim'))
print("ANNA (BYT):",byt.get_daysOverdue('Anna'))
print("ANNA (SKAZAT):", skazat.get_daysOverdue('Anna'))
print("SETTING STUDY INTERVAL TO TWO WEEKS SO THAT THE VERBS ARE DUE TODAY")
byt.lastInterval['Tim'] = 14
byt.lastInterval['Anna'] = 14
skazat.lastInterval['Tim'] = 14
skazat.lastInterval['Anna'] = 14
byt.set_dueDate('Tim')
byt.set_dueDate('Anna')
skazat.set_dueDate('Anna')
skazat.set_dueDate('Tim')
print('GET NEXT STUDY DATE FUNCTIONS SHOULD NOW RETURN DUE TODAY')
print("GET NEXT STUDY DATE FUNCTION TIM (BYT)")
print(byt.get_nextStudyDate('Tim'))
print("GET NEXT STUDY DATE FUNCTION TIM (SKAZAT)")
print(skazat.get_nextStudyDate('Tim'))
print("GET NEXT STUDY DATE FUNCTION ANNA (BYT)")
print(byt.get_nextStudyDate('Anna'))
print("GET NEXT STUDY DATE FUNCTION ANNA (SKAZAT)")
print(skazat.get_nextStudyDate('Anna'))
print("SETTING STUDY INTERVAL TO 5 WEEKS SO THAT THE VERBS ARE DUE IN THREE WEEKS")
byt.lastInterval['Tim'] = 35
byt.lastInterval['Anna'] = 35
skazat.lastInterval['Tim'] = 35
skazat.lastInterval['Anna'] = 35
byt.set_dueDate('Tim')
byt.set_dueDate('Anna')
skazat.set_dueDate('Tim')
skazat.set_dueDate('Anna')
print("GET NEXT STUDY DATE FUNCTION TIM (BYT)")
print(byt.get_nextStudyDate('Tim'))
print("GET NEXT STUDY DATE FUNCTION TIM (SKAZAT)")
print(skazat.get_nextStudyDate('Tim'))
print("GET NEXT STUDY DATE FUNCTION ANNA (BYT)")
print(byt.get_nextStudyDate('Anna'))
print("GET NEXT STUDY DATE FUNCTION ANNA (SKAZAT)")
print(skazat.get_nextStudyDate('Anna'))
print("GET DAYS OVERDUE - SHOULD RETURN AN INT < 0")
print("TIM (BYT):",byt.get_daysOverdue('Tim'))
print("TIM (SKAZAT):",skazat.get_daysOverdue('Tim'))
print("ANNA (BYT):",byt.get_daysOverdue('Anna'))
print("ANNA (SKAZAT):", skazat.get_daysOverdue('Anna'))
fileList = os.listdir('./verbs')
fileList.sort()

#for file in fileList:
#    if file[-4:] == '.txt':
#        with shelve.open('./verbs/verbsDB') as verbShelf:
#            verbShelf[file:-4] = verb(file)
