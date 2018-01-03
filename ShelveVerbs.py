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
            self.users = []

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
    def get_examplesList(self, stripPunctuation=False, toLower=False):
        """takes an optional parameter to strip punctuation marks; returns a list of the russian example sentences; the indices for these match the indices in the corresponding translation list"""
        if not stripPunctuation and not toLower:
            return self.examplesList
        else:

            strippedList = self.examplesList[:]
            if stripPunctuation:
                for i in range(len(strippedList)):
                    strippedList[i] = strippedList[i].replace(',','')
                    strippedList[i] = strippedList[i].replace('.','')
                    strippedList[i] = strippedList[i].replace(':','')
                    strippedList[i] = strippedList[i].replace(';','')
                    strippedList[i] = strippedList[i].replace('?','')
                    strippedList[i] = strippedList[i].replace('!','')
            if toLower:
                for i in range(len(strippedList)):
                    strippedList[i] = strippedList[i].lower()
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
    def addUser(self, user, overwrite=False):
        """user - user to be added; overwrite - optional parameter (False by default) - if set to true, will reset SM2 values for given user name if that user already exists;
        otherwise, if the specified user is not already loaded, adds a user to the dictionaries used for the spaced repetition algorithm and preloads default values in these dictionaries"""
        if not overwrite:
            if user not in self.users:
                self.users.append(user)
                self.easinessFactor[user] = 2.5
                self.lastInterval[user] = 1
                self.previouslyStudied [user] = False
                self.dateLastStudied[user] = QtCore.QDate.currentDate()
                self.dueDate[user] = self.dateLastStudied[user].addDays(self.lastInterval[user])
        else:
            if user not in self.users:
                self.users.append(user)
            self.easinessFactor[user] = 2.5
            self.lastInterval[user] = 1
            self.previouslyStudied [user] = False
            self.dateLastStudied[user] = QtCore.QDate.currentDate()
            self.dueDate[user] = self.dateLastStudied[user].addDays(self.lastInterval[user])

    def was_previouslyStudied(self, user):
        """returns the value of self.previouslyStudied for the user specified; used to determine whether a user should be presented with familiarization
        screens prior to quiz initiation"""
        return self.previouslyStudied.get(user, False)
    def was_studiedToday(self,user):
        """returns True if a user last studied a verb today; False otherwise"""
        if not self.was_previouslyStudied(user):
            return False
        elif self.was_previouslyStudied(user) and self.dateLastStudied[user] == QtCore.QDate.currentDate():
            return True
        else:
            return False
    def update_study_interval(self, user, score):
        """user - a string of the name of the user whose interval is to be updated; score - a number between 0 and 1 representing performance on quiz;
        updates the desired study interval for the user (self.easinessFactor and self.lastInterval) using the SM2 algorithm"""

        if not self.was_studiedToday(user): #only update interval per SM2 algorithm if this is the first time the user is studying the verb today
            self.previouslyStudied[user] = True
            self.set_dateLastStudied(user)
            if (score*5) < 3.5:
                self.lastInterval[user] = 1
            else:
                if self.lastInterval.get(user, 1) == 1:
                    print('user interval is 1; setting to 2')
                    self.lastInterval[user] = 2
                    print(self.lastInterval[user])
                elif self.lastInterval[user] == 2:
                    print('user interval is 2; setting to 4')
                    self.lastInterval[user] = 4
                    print(self.lastInterval[user])
                else:
                    print('user interval was greater than 2; using sm2 algorimthm')
                    print('prior easiness factor:',self.easinessFactor[user])
                    self.easinessFactor[user] += (0.1-(5-(score*5))*(0.08+(5-(score*5))*0.02))
                    if self.easinessFactor[user] < 1.3:
                        self.easinessFactor[user] = 1.3
                    print('new easiness factor:',self.easinessFactor[user])
                    print('old interval:',self.lastInterval[user])
                    self.lastInterval[user] *= self.easinessFactor[user]
                    self.lastInterval[user] = int(self.lastInterval[user])
                    print('new interval:',self.lastInterval[user])
            self.dueDate[user] = self.dateLastStudied[user].addDays(self.lastInterval[user])
        else: #if the user studies the verb for a second or greater time and scores 0.7 or above, simply add one to the due date - this will prevent the
        # user from studying a verb a ton of times in one day to dramatically increase the study interval
            self.previouslyStudied[user] = True
            self.set_dateLastStudied(user)
            if (score*5) < 3.5:
                self.lastInterval[user] = 1
            else:
                self.lastInterval[user] += 1
                self.dueDate[user] = self.dateLastStudied[user].addDays(self.lastInterval[user])
    def set_dateLastStudied(self, user, date=QtCore.QDate.currentDate()):
        """user - the user whose date last studied you want to set; date - QDate object - defaults to current date;
        updates dateLastStudied for the specified user to the specified date"""
        self.dateLastStudied[user] = date
    def get_dateLastStudied(self, user):
        """user - the user whose dateLastStudied you wish to retrieve; returns a Qstring of the date last studied"""
        dateRequested = self.dateLastStudied.get(user, QtCore.QDate.currentDate())
        return dateRequested.toString('MM.dd.yyyy')
    def get_nextStudyDateDisplay(self,user):
        """returns a string indicating the status of a current verb for a given user;
        if the verb is overdue, returns "# days overdue" where # is the days overdue;
        if the user has not yet studied a verb returns the phrase 'Not yet studied';
        if the verb is due on the day it is being viewed, returns 'Due today!';
        if the verb has been studied but is not yet due, returns the due date in mm.dd.yyyy format"""
        if not self.was_previouslyStudied(user):
            return "Not yet studied"
        else:
            if self.is_overdue(user):
                return str(self.get_daysOverdue(user)) + " days overdue"
            else:
                displayDate = self.dueDate[user]
                if displayDate == QtCore.QDate.currentDate():
                    return("Due today!")
                return displayDate.toString('MM.dd.yyyy')
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
    def get_dueDate(self,user,stringFormat=True):
        """returns a the due date for a verb for the given user in Qstring mm.dd.yyyy format"""
        return self.dueDate[user].toString('MM.dd.yyyy')
    def set_dueDate(self,user):
        self.dueDate[user] = self.dateLastStudied[user].addDays(self.lastInterval[user])

#testing -----
# delimiter = '=========================================='
# byt = verb('0001byt.txt')
# skazat = verb('0002skazat.txt')
# print(delimiter)
# print('PRINT ENTIRE CONJUGATION INFO FOR BYT')
# print(byt)
# print(delimiter)
# print('PRINT ENTIRE CONJUGATION INFO FOR SKAZAT')
# print(skazat)
# print(delimiter)
# print("INFINITIVE GETTER; BYT THEN SKAZAT")
# print(byt.get_infinitive())
# print(skazat.get_infinitive())
# print(delimiter)
# print('ASPECT GETTER: BYT THEN SKAZAT')
# print(byt.get_aspect())
# print(skazat.get_aspect())
# print(delimiter)
# print('FREQUENCY GETTER; BYT THEN SKAZAT')
# print(byt.get_frequencyRank())
# print(skazat.get_frequencyRank())
# print(delimiter)
# print('MEANING GETTER; BYT THEN SKAZAT')
# print(byt.get_meaning())
# print(skazat.get_meaning())
# print(delimiter)
# print('INDICATIVE FIRST SINGULAR GETTER; BYT THEN SKAZAT')
# print(byt.get_indicativeFirstSg())
# print(skazat.get_indicativeFirstSg())
# print(delimiter)
# print('INDICATIVE SECOND PERSON SINGULAR; BYT THEN SKAZAT')
# print(byt.get_indicativeSecondSg())
# print(skazat.get_indicativeSecondSg())
# print(delimiter)
# print('INDICATIVE THIRD PERSON PLURAL; BYT THEN SKAZAT')
# print(byt.get_indicativeThirdSg())
# print(skazat.get_indicativeThirdSg())
# print(delimiter)
# print('INDICATIVE 1ST PERSON PLURAL: BYT THEN SKAZAT')
# print(byt.get_indicativeFirstPl())
# print(skazat.get_indicativeFirstPl())
# print(delimiter)
# print('INDICATIVE 2ND PERSON PLURAL; BYT THEN SKAZAT')
# print(byt.get_indicativeSecondPl())
# print(skazat.get_indicativeSecondPl())
# print(delimiter)
# print('INDICATIVE 3RD PERSON PLURAL;BYT THEN SKAZAT')
# print(byt.get_indicativeThirdPl())
# print(skazat.get_indicativeThirdPl())
# print(delimiter)
# print('IMPERATIVE SINGULAR; BYT THEN SKAZAT')
# print(byt.get_imperativeSg())
# print(skazat.get_imperativeSg())
# print(delimiter)
# print('IMPERATIVE PLURAL; BYT THEN SKAZAT')
# print(byt.get_imperativePl())
# print(skazat.get_imperativePl())
# print(delimiter)
# print('PAST MASCULINE; BYT THEN SKAZAT')
# print(byt.get_pastMasc())
# print(skazat.get_pastMasc())
# print(delimiter)
# print('PAST FEMININE; BYT THEN SKAZAT')
# print(byt.get_pastFem())
# print(skazat.get_pastFem())
# print(delimiter)
# print('PAST NEUTER; BYT THEN SKAZAT')
# print(byt.get_pastNeut())
# print(skazat.get_pastNeut())
# print(delimiter)
# print('PAST PLURAL; BYT THEN SKAZAT')
# print(byt.get_pastPl())
# print(skazat.get_pastPl())
# print(delimiter)
# print('Examples List Functionality; Print each example, each example stripped of punctuation, each example stripped of punctuation in lower case, each example in lower case, its translation, and then the file name for the corresponding audio; byt then skazat')
# bytExList = byt.get_examplesList()
# bytExListStripped = byt.get_examplesList(True,False)
# bytExListStrippedLower = byt.get_examplesList(True,True)
# bytExListLower = byt.get_examplesList(False,True)
# bytTransList = byt.get_examplesListTranslations()
# bytFileList = byt.get_verbAudioList()
# skazatExList = skazat.get_examplesList()
# skazatExListStripped = skazat.get_examplesList(True)
# skazatExListStrippedLower = skazat.get_examplesList(True,True)
# skazatExListLower = skazat.get_examplesList(False,True)
# skazatTransList = skazat.get_examplesListTranslations()
# skazatFileList = skazat.get_verbAudioList()
# print(delimiter)
# for i in range(len(bytExList)):
#     print(bytExList[i])
#     print(bytExListStripped[i])
#     print(bytExListStrippedLower[i])
#     print(bytExListLower[i])
#     print(bytTransList[i])
#     print(bytFileList[i])
#     print(delimiter)
# for i in range(len(skazatExList)):
#     print(skazatExList[i])
#     print(skazatExListStripped[i])
#     print(skazatExListStrippedLower[i])
#     print(skazatExListLower[i])
#     print(skazatTransList[i])
#     print(skazatFileList[i])
#     print(delimiter)
# print("CONJUGATION AUDIO FOR BYT AND SKAZAT")
# print(byt.get_conjugationAudio())
# print(skazat.get_conjugationAudio())
# print(delimiter)
# print("RANDOMIZED STRIPPED EXAMPLES; BYT AND SKAZAT")
# bytRandomExList = byt.get_randomizedExamplesList()
# skazatRandomExList = skazat.get_randomizedExamplesList()
# for example in bytRandomExList:
#     print(example)
# print(delimiter)
# for example in skazatRandomExList:
#     print(example)
# print(delimiter)
# print("USER BASED TESTS - USERS TIM AND ANNA")
# byt.addUser('Tim')
# skazat.addUser('Tim')
# byt.addUser('Anna')
# skazat.addUser('Anna')
# print("BEFORE STUDY; WAS PREVIOUSLY STUDIED SHOULD RETURN FALSE")
# print("TIM (BYT):", byt.was_previouslyStudied('Tim'))
# print("ANNA (BYT):", byt.was_previouslyStudied('Anna'))
# print("TIM (SKAZAT):", skazat.was_previouslyStudied('Tim'))
# print("ANNA (SKAZAT):", skazat.was_previouslyStudied('Anna'))
# print("DUE DATE SHOULD BE INTIALIZED FOR THESE USERS TO ONE DAY FROM NOW")
# print("TIM (BYT):", byt.get_dueDate('Tim'))
# print("ANNA (BYT):", byt.get_dueDate('Anna'))
# print("TIM (SKAZAT):", skazat.get_dueDate('Tim'))
# print("ANNA (SKAZAT):", skazat.get_dueDate('Anna'))
# print("TIM AND ANNA STUDY BYT AND SKAZAT AND SCORE 80")
# byt.update_study_interval('Tim',0.8)
# byt.update_study_interval('Anna',0.8)
# skazat.update_study_interval('Tim',0.8)
# skazat.update_study_interval('Anna',0.8)
# print("WAS PREVIOUSLY STUDIED SHOULD NOW RETURN TRUE")
# print("TIM (BYT):", byt.was_previouslyStudied('Tim'))
# print("ANNA (BYT):", byt.was_previouslyStudied('Anna'))
# print("TIM (SKAZAT):", skazat.was_previouslyStudied('Tim'))
# print("ANNA (SKAZAT):", skazat.was_previouslyStudied('Anna'))
# print("DUE DATE SHOULD BE UPDATED FROM PREVIOUS VALUE:")
# print("TIM (BYT):", byt.get_dueDate('Tim'))
# print("ANNA (BYT):", byt.get_dueDate('Anna'))
# print("TIM (SKAZAT):", skazat.get_dueDate('Tim'))
# print("ANNA (SKAZAT):", skazat.get_dueDate('Anna'))
# print("IS OVERDUE SHOULD RETURN FALSE")
# print("TIM (BYT):", byt.is_overdue('Tim'))
# print("TIM (SKAZAT):", skazat.is_overdue('Tim'))
# print("ANNA (BYT):",byt.is_overdue('Anna'))
# print("ANNA (SKAZAT):",skazat.is_overdue('Anna'))
# print("TESTING SETTING AND GETTING DATE; SET DATE LAST STUDIED TO 2 WEEKS AGO")
# twoWeeksAgo = QtCore.QDate.currentDate()
# twoWeeksAgo = twoWeeksAgo.addDays(-14)
# byt.set_dateLastStudied('Tim',twoWeeksAgo)
# byt.set_dateLastStudied('Anna',twoWeeksAgo)
# skazat.set_dateLastStudied('Tim',twoWeeksAgo)
# skazat.set_dateLastStudied('Anna',twoWeeksAgo)
# byt.set_dueDate('Tim')
# byt.set_dueDate('Anna')
# skazat.set_dueDate('Tim')
# skazat.set_dueDate('Anna')
# print("TIM (BYT) - SHOULD RETURN TWO WEEKS AGO")
# print(byt.get_dateLastStudied('Tim'))
# print('TIM (SKAZAT) - SHOULD RETURN TWO WEEKS AGO')
# print(skazat.get_dateLastStudied('Tim'))
# print('ANNA (BYT) - SHOULD RETURN TWO WEEKS AGO')
# print(byt.get_dateLastStudied('Anna'))
# print('ANNA (SKAZAT) - SHOULD RETURN TWO WEEKS AGO')
# print(skazat.get_dateLastStudied('Anna'))
# print("BYT AND SKAZAT SHOULD BOTH BE OVERDUE NOW THAT THE DATE LAST STUDIED HAS BEEN SET TO TWO WEEKS AGO")
# print("GET NEXT STUDY DATE FOR TIM (BYT) - SHOULD RETURN OVERDUE")
# print(byt.get_nextStudyDateDisplay('Tim'))
# print("GET NEXT STUDY DATE FOR TIM (SKAZAT) - SHOULD RETURN OVERDUE")
# print(skazat.get_nextStudyDateDisplay('Tim'))
# print("GET NEXT STUDY DATE FOR ANNA (BYT) - SHOULD RETURN OVERDUE")
# print(byt.get_nextStudyDateDisplay('Anna'))
# print("GET NEXT STUDY DATE FOR ANNA (SKAZAT) - SHOULD RETURN OVERDUE")
# print(skazat.get_nextStudyDateDisplay('Anna'))
# print("IS OVERDUE FUNCTION TIM (BYT) - SHOULD RETURN TRUE")
# print(byt.is_overdue('Tim'))
# print("IS OVERDUE FUNCTION TIM (SKAZAT) - SHOULD RETURN TRUE")
# print(skazat.is_overdue('Tim'))
# print("IS OVERDUE FUNCTION ANNA (BYT) - SHOULD RETURN TRUE")
# print(byt.is_overdue('Anna'))
# print("IS OVERDUE FUNCTION ANNA (SKAZAT) - SHOULD RETURN TRUE")
# print(skazat.is_overdue('Anna'))
# print("GET DAYS OVERDUE; SHOULD RETURN AN INT > 0")
# print("TIM (BYT):",byt.get_daysOverdue('Tim'))
# print("TIM (SKAZAT):",skazat.get_daysOverdue('Tim'))
# print("ANNA (BYT):",byt.get_daysOverdue('Anna'))
# print("ANNA (SKAZAT):", skazat.get_daysOverdue('Anna'))
# print("SETTING STUDY INTERVAL TO TWO WEEKS SO THAT THE VERBS ARE DUE TODAY")
# byt.lastInterval['Tim'] = 14
# byt.lastInterval['Anna'] = 14
# skazat.lastInterval['Tim'] = 14
# skazat.lastInterval['Anna'] = 14
# byt.set_dueDate('Tim')
# byt.set_dueDate('Anna')
# skazat.set_dueDate('Anna')
# skazat.set_dueDate('Tim')
# print('GET NEXT STUDY DATE FUNCTIONS SHOULD NOW RETURN DUE TODAY')
# print("GET NEXT STUDY DATE FUNCTION TIM (BYT)")
# print(byt.get_nextStudyDateDisplay('Tim'))
# print("GET NEXT STUDY DATE FUNCTION TIM (SKAZAT)")
# print(skazat.get_nextStudyDateDisplay('Tim'))
# print("GET NEXT STUDY DATE FUNCTION ANNA (BYT)")
# print(byt.get_nextStudyDateDisplay('Anna'))
# print("GET NEXT STUDY DATE FUNCTION ANNA (SKAZAT)")
# print(skazat.get_nextStudyDateDisplay('Anna'))
# print("SETTING STUDY INTERVAL TO 5 WEEKS SO THAT THE VERBS ARE DUE IN THREE WEEKS")
# byt.lastInterval['Tim'] = 35
# byt.lastInterval['Anna'] = 35
# skazat.lastInterval['Tim'] = 35
# skazat.lastInterval['Anna'] = 35
# byt.set_dueDate('Tim')
# byt.set_dueDate('Anna')
# skazat.set_dueDate('Tim')
# skazat.set_dueDate('Anna')
# print("GET NEXT STUDY DATE FUNCTION TIM (BYT)")
# print(byt.get_nextStudyDateDisplay('Tim'))
# print("GET NEXT STUDY DATE FUNCTION TIM (SKAZAT)")
# print(skazat.get_nextStudyDateDisplay('Tim'))
# print("GET NEXT STUDY DATE FUNCTION ANNA (BYT)")
# print(byt.get_nextStudyDateDisplay('Anna'))
# print("GET NEXT STUDY DATE FUNCTION ANNA (SKAZAT)")
# print(skazat.get_nextStudyDateDisplay('Anna'))
# print("GET DAYS OVERDUE - SHOULD RETURN AN INT < 0")
# print("TIM (BYT):",byt.get_daysOverdue('Tim'))
# print("TIM (SKAZAT):",skazat.get_daysOverdue('Tim'))
# print("ANNA (BYT):",byt.get_daysOverdue('Anna'))
# print("ANNA (SKAZAT):", skazat.get_daysOverdue('Anna'))
# print(delimiter)
# print("SET DATE LAST STUDIED TO TODAY AND INTERVAL TO 2 WEEKS; SET DUE DATE, GET DUE DATE, GET DAYS OVERDUE, TEST IS OVERDUE, AND GET NEXT STUDY DATE")
# byt.set_dateLastStudied('Tim')
# byt.set_dateLastStudied('Anna')
# skazat.set_dateLastStudied('Tim')
# skazat.set_dateLastStudied('Anna')
# byt.lastInterval['Tim'] = 14
# byt.lastInterval['Anna'] = 14
# skazat.lastInterval['Tim'] = 14
# skazat.lastInterval['Anna'] = 14
# byt.set_dueDate('Tim')
# skazat.set_dueDate('Tim')
# byt.set_dueDate('Anna')
# skazat.set_dueDate('Anna')
# print("TIM'S DUE DATE AND DAYS OVERDUE (BYT):")
# print(byt.get_dueDate('Tim'))
# print(byt.get_daysOverdue('Tim'))
# print('is overdue:', byt.is_overdue('Tim'))
# print("ANNA'S DUE DATE AND DAYS OVERDUE (BYT):")
# print(byt.get_dueDate('Anna'))
# print(byt.get_daysOverdue('Anna'))
# print('is overdue:', byt.is_overdue('Anna'))
# print("TIM'S DUE DATE AND DAYS OVERDUE (SKAZAT):")
# print(skazat.get_dueDate('Tim'))
# print(skazat.get_daysOverdue('Tim'))
# print('is overdue:', skazat.is_overdue('Tim'))
# print("ANNA'S DUE DATE AND DAYS OVERDUE (SKAZAT):")
# print(skazat.get_dueDate('Anna'))
# print(skazat.get_daysOverdue('Anna'))
# print('is overdue:', skazat.is_overdue('Anna'))
# print(delimiter)
# print("Try readding Tim and Anna as users with default overwite=False")
# byt.addUser('Tim')
# byt.addUser('Anna')
# skazat.addUser('Tim')
# skazat.addUser('Anna')
# print("TIM'S DUE DATE AND DAYS OVERDUE (BYT) - SHOULD NOT HAVE CHANGED:")
# print(byt.get_dueDate('Tim'))
# print(byt.get_daysOverdue('Tim'))
# print('is overdue:',byt.is_overdue('Tim'))
# print("ANNA'S DUE DATE AND DAYS OVERDUE (BYT) - SHOULD NOT HAVE CHANGED:")
# print(byt.get_dueDate('Anna'))
# print(byt.get_daysOverdue('Anna'))
# print('is overdue:', byt.is_overdue('Anna'))
# print("TIM'S DUE DATE AND DAYS OVERDUE (SKAZAT) - SHOULD NOT HAVE CHANGED:")
# print(skazat.get_dueDate('Tim'))
# print(skazat.get_daysOverdue('Tim'))
# print('is overdue:', skazat.is_overdue('Tim'))
# print("ANNA'S DUE DATE AND DAYS OVERDUE (SKAZAT) - SHOULD NOT HAVE CHANGED:")
# print(skazat.get_dueDate('Anna'))
# print(skazat.get_daysOverdue('Anna'))
# print('is overdue:', skazat.is_overdue('Anna'))
# print(delimiter)
# print('Try readding Tim and Anna as users with overwrite=True')
# byt.addUser('Tim',overwrite=True)
# byt.addUser('Anna',overwrite=True)
# skazat.addUser('Tim',overwrite=True)
# skazat.addUser('Anna',overwrite=True)
# print("TIM'S DUE DATE AND DAYS OVERDUE (BYT) - SHOULD HAVE CHANGED:")
# print(byt.get_dueDate('Tim'))
# print(byt.get_daysOverdue('Tim'))
# print('is overdue:',byt.is_overdue('Tim'))
# print("ANNA'S DUE DATE AND DAYS OVERDUE (BYT) - SHOULD HAVE CHANGED:")
# print(byt.get_dueDate('Anna'))
# print(byt.get_daysOverdue('Anna'))
# print('is overdue:', byt.is_overdue('Anna'))
# print("TIM'S DUE DATE AND DAYS OVERDUE (SKAZAT) - SHOULD HAVE CHANGED:")
# print(skazat.get_dueDate('Tim'))
# print(skazat.get_daysOverdue('Tim'))
# print('is overdue:', skazat.is_overdue('Tim'))
# print("ANNA'S DUE DATE AND DAYS OVERDUE (SKAZAT) - SHOULD HAVE CHANGED:")
# print(skazat.get_dueDate('Anna'))
# print(skazat.get_daysOverdue('Anna'))
# print('is overdue:', skazat.is_overdue('Anna'))

# #additional user testing
# print('Add user named "A"')
# byt.addUser('A')
# skazat.addUser('A')
# print('Test to see whether user document for A is properly initialized')
# print("User list - should now contain A")
# print('byt',byt.users)
# print('skazat',skazat.users)
# print('Easiness factor - should default to 2.5')
# print('byt',byt.easinessFactor['A'])
# print('skazat',skazat.easinessFactor['A'])
# print('last interval - should default to 1')
# print('byt',byt.lastInterval['A'])
# print('skazat',skazat.lastInterval['A'])
# print('previously studied - should default to False')
# print('byt',byt.previouslyStudied['A'])
# print('skazat',skazat.previouslyStudied['A'])
# print('date last studied - should default to today')
# print('byt',byt.dateLastStudied['A'])
# print('skazat',skazat.dateLastStudied['A'])
# print('due date - should default to one day from now')
# print('byt',byt.dueDate['A'])
# print('skazat',skazat.dueDate['A'])
# print('Test the was_studiedToday function; should return false')
# print('byt',byt.was_studiedToday('A'))
# print('skazat',skazat.was_studiedToday('A'))
# print('user A studies byt 6 times in one day, scoring 85 on each review')
# byt.update_study_interval('A',.85)
# print('after 1 - new due date for byt:',byt.get_dueDate('A'))
# byt.update_study_interval('A',.85)
# print('after 2 - new due date for byt:',byt.get_dueDate('A'))
# byt.update_study_interval('A',.85)
# print('after 3 - new due date for byt:',byt.get_dueDate('A'))
# byt.update_study_interval('A',.85)
# print('after 4 - new due date for byt:',byt.get_dueDate('A'))
# byt.update_study_interval('A',.85)
# print('after 5 - new due date for byt:',byt.get_dueDate('A'))
# byt.update_study_interval('A',.85)
# print("user A's new due date for byt:",byt.get_dueDate('A'))
# print('user A studies skazat 6 times in one day, scoring 85 on each review')
# skazat.update_study_interval('A',.85)
# print('after 1 - new due date for skazat:',skazat.get_dueDate('A'))
# skazat.update_study_interval('A',.85)
# print('after 2 - new due date for skazat:',skazat.get_dueDate('A'))
# skazat.update_study_interval('A',.85)
# print('after 3 - new due date for skazat:',skazat.get_dueDate('A'))
# skazat.update_study_interval('A',.85)
# print('after 4 - new due date for skazat:',skazat.get_dueDate('A'))
# skazat.update_study_interval('A',.85)
# print('after 5 - new due date for skazat:',skazat.get_dueDate('A'))
# skazat.update_study_interval('A',.85)
# print("user A's new due date for skazat:",skazat.get_dueDate('A'))
# print("test the was_studiedToday function - should now return True")
# print('byt',byt.was_studiedToday('A'))
# print('skazat',skazat.was_studiedToday('A'))
#
# print(delimiter)
# print('Resetting user A')
# byt.addUser('A',overwrite=True)
# skazat.addUser('A',overwrite=True)
# print('user A studies byt 6 times in one day, scoring 90 on each review -reviews after the initial review should only increase due date by one day')
# byt.update_study_interval('A',.90)
# print('after 1 - new due date for byt:',byt.get_dueDate('A'))
# byt.update_study_interval('A',.90)
# print('after 2 - new due date for byt:',byt.get_dueDate('A'))
# byt.update_study_interval('A',.90)
# print('after 3 - new due date for byt:',byt.get_dueDate('A'))
# byt.update_study_interval('A',.90)
# print('after 4 - new due date for byt:',byt.get_dueDate('A'))
# byt.update_study_interval('A',.90)
# print('after 5 - new due date for byt:',byt.get_dueDate('A'))
# byt.update_study_interval('A',.90)
# print("user A's new due date for byt:",byt.get_dueDate('A'))
# print('user A studies skazat 6 times in one day, scoring 90 on each review -reviews after the initial review should only increase due date by one day')
# skazat.update_study_interval('A',.90)
# print('after 1 - new due date for skazat:',skazat.get_dueDate('A'))
# skazat.update_study_interval('A',.90)
# print('after 2 - new due date for skazat:',skazat.get_dueDate('A'))
# skazat.update_study_interval('A',.90)
# print('after 3 - new due date for skazat:',skazat.get_dueDate('A'))
# skazat.update_study_interval('A',.90)
# print('after 4 - new due date for skazat:',skazat.get_dueDate('A'))
# skazat.update_study_interval('A',.90)
# print('after 5 - new due date for skazat:',skazat.get_dueDate('A'))
# skazat.update_study_interval('A',.90)
# print("user A's new due date for skazat:",skazat.get_dueDate('A'))
# threeWeeksAgo = QtCore.QDate.currentDate().addDays(-21)
# print('resetting user A')
# byt.addUser('A',overwrite=True)
# skazat.addUser('A',overwrite=True)
# print('setting date last studied to 3 weeks ago and study interval to 16 days')
# byt.set_dateLastStudied('A',threeWeeksAgo)
# skazat.set_dateLastStudied('A',threeWeeksAgo)
# print('byt',byt.dateLastStudied['A'])
# print('skazat',skazat.dateLastStudied['A'])
# print('set last interval to 18 days')
# byt.lastInterval['A'] = 18
# byt.set_dueDate('A')
# skazat.lastInterval['A'] = 18
# skazat.set_dueDate('A')
# print('user A scores 85 on tests')
# print('byt was studied today:', byt.was_studiedToday('A'))
# byt.update_study_interval('A',.85)
# skazat.update_study_interval('A',.85)
# print('new interval for byt', byt.lastInterval['A'])
# print('new interval for skazat', skazat.lastInterval['A'])
# print('new due date for byt:',byt.get_dueDate('A'))
# print('new due date for skazat:',skazat.get_dueDate('A'))
# print('user A scores 85 on tests again - interval should only increase by 1')
# byt.update_study_interval('A',.85)
# skazat.update_study_interval('A',.85)
# print('new interval for byt', byt.lastInterval['A'])
# print('new interval for skazat', skazat.lastInterval['A'])
# print('new due date for byt:',byt.get_dueDate('A'))
# print('new due date for skazat:',skazat.get_dueDate('A'))
# print(delimiter)
# print(delimiter)
# print('INCREASE LAST INTERVAL WHILE KEEPING EASINESS FACTOR CONSTANT')
#
# print(delimiter)
# print('resetting user A')
# byt.addUser('A',overwrite=True)
# skazat.addUser('A',overwrite=True)
# print('set last interval to 2 days')
# byt.lastInterval['A'] = 2
# byt.set_dueDate('A')
# skazat.lastInterval['A'] = 2
# skazat.set_dueDate('A')
# print('user A scores 85 on tests')
# byt.update_study_interval('A',.85)
# skazat.update_study_interval('A',.85)
# print('new interval for byt', byt.lastInterval['A'])
# print('new interval for skazat', skazat.lastInterval['A'])
# print('new due date for byt:',byt.get_dueDate('A'))
# print('new due date for skazat:',skazat.get_dueDate('A'))
#
# print(delimiter)
# print('resetting user A')
# byt.addUser('A',overwrite=True)
# skazat.addUser('A',overwrite=True)
# print('set last interval to 3 days')
# byt.lastInterval['A'] = 3
# byt.set_dueDate('A')
# skazat.lastInterval['A'] = 3
# skazat.set_dueDate('A')
# print('user A scores 85 on tests')
# byt.update_study_interval('A',.85)
# skazat.update_study_interval('A',.85)
# print('new interval for byt', byt.lastInterval['A'])
# print('new interval for skazat', skazat.lastInterval['A'])
# print('new due date for byt:',byt.get_dueDate('A'))
# print('new due date for skazat:',skazat.get_dueDate('A'))
#
# print(delimiter)
# print('resetting user A')
# byt.addUser('A',overwrite=True)
# skazat.addUser('A',overwrite=True)
# print('set last interval to 4 days')
# byt.lastInterval['A'] = 4
# byt.set_dueDate('A')
# skazat.lastInterval['A'] = 4
# skazat.set_dueDate('A')
# print('user A scores 85 on tests')
# byt.update_study_interval('A',.85)
# skazat.update_study_interval('A',.85)
# print('new interval for byt', byt.lastInterval['A'])
# print('new interval for skazat', skazat.lastInterval['A'])
# print('new due date for byt:',byt.get_dueDate('A'))
# print('new due date for skazat:',skazat.get_dueDate('A'))
#
# print(delimiter)
# print('resetting user A')
# byt.addUser('A',overwrite=True)
# skazat.addUser('A',overwrite=True)
# print('set last interval to 5 days')
# byt.lastInterval['A'] = 5
# byt.set_dueDate('A')
# skazat.lastInterval['A'] = 5
# skazat.set_dueDate('A')
# print('user A scores 85 on tests')
# byt.update_study_interval('A',.85)
# skazat.update_study_interval('A',.85)
# print('new interval for byt', byt.lastInterval['A'])
# print('new interval for skazat', skazat.lastInterval['A'])
# print('new due date for byt:',byt.get_dueDate('A'))
# print('new due date for skazat:',skazat.get_dueDate('A'))
#
# print(delimiter)
# print('resetting user A')
# byt.addUser('A',overwrite=True)
# skazat.addUser('A',overwrite=True)
# print('set last interval to 6 days')
# byt.lastInterval['A'] = 6
# byt.set_dueDate('A')
# skazat.lastInterval['A'] = 6
# skazat.set_dueDate('A')
# print('user A scores 85 on tests')
# byt.update_study_interval('A',.85)
# skazat.update_study_interval('A',.85)
# print('new interval for byt', byt.lastInterval['A'])
# print('new interval for skazat', skazat.lastInterval['A'])
# print('new due date for byt:',byt.get_dueDate('A'))
# print('new due date for skazat:',skazat.get_dueDate('A'))
#
# print(delimiter)
# print('resetting user A')
# byt.addUser('A',overwrite=True)
# skazat.addUser('A',overwrite=True)
# print('set last interval to 7 days')
# byt.lastInterval['A'] = 7
# byt.set_dueDate('A')
# skazat.lastInterval['A'] = 7
# skazat.set_dueDate('A')
# print('user A scores 85 on tests')
# byt.update_study_interval('A',.85)
# skazat.update_study_interval('A',.85)
# print('new interval for byt', byt.lastInterval['A'])
# print('new interval for skazat', skazat.lastInterval['A'])
# print('new due date for byt:',byt.get_dueDate('A'))
# print('new due date for skazat:',skazat.get_dueDate('A'))
#
# print(delimiter)
# print(delimiter)
# print('INCREASE LAST INTERVAL WHILE KEEPING EASINESS FACTOR CONSTANT - LOWEST STARTING EASINESS FACTOR')
# print(delimiter)
# print('resetting user A')
# byt.addUser('A',overwrite=True)
# skazat.addUser('A',overwrite=True)
# byt.easinessFactor['A'] = 1.3
# skazat.easinessFactor['A'] = 1.3
# print('set last interval to 2 days')
# byt.lastInterval['A'] = 2
# byt.set_dueDate('A')
# skazat.lastInterval['A'] = 2
# skazat.set_dueDate('A')
# print('user A scores 85 on tests')
# byt.update_study_interval('A',.85)
# skazat.update_study_interval('A',.85)
# print('new interval for byt', byt.lastInterval['A'])
# print('new interval for skazat', skazat.lastInterval['A'])
# print('new due date for byt:',byt.get_dueDate('A'))
# print('new due date for skazat:',skazat.get_dueDate('A'))
#
# print(delimiter)
# print('resetting user A')
# byt.addUser('A',overwrite=True)
# skazat.addUser('A',overwrite=True)
# byt.easinessFactor['A'] = 1.3
# skazat.easinessFactor['A'] = 1.3
# print('set last interval to 3 days')
# byt.lastInterval['A'] = 3
# byt.set_dueDate('A')
# skazat.lastInterval['A'] = 3
# skazat.set_dueDate('A')
# print('user A scores 85 on tests')
# byt.update_study_interval('A',.85)
# skazat.update_study_interval('A',.85)
# print('new interval for byt', byt.lastInterval['A'])
# print('new interval for skazat', skazat.lastInterval['A'])
# print('new due date for byt:',byt.get_dueDate('A'))
# print('new due date for skazat:',skazat.get_dueDate('A'))
#
# print(delimiter)
# print('resetting user A')
# byt.addUser('A',overwrite=True)
# skazat.addUser('A',overwrite=True)
# byt.easinessFactor['A'] = 1.3
# skazat.easinessFactor['A'] = 1.3
# print('set last interval to 4 days')
# byt.lastInterval['A'] = 4
# byt.set_dueDate('A')
# skazat.lastInterval['A'] = 4
# skazat.set_dueDate('A')
# print('user A scores 85 on tests')
# byt.update_study_interval('A',.85)
# skazat.update_study_interval('A',.85)
# print('new interval for byt', byt.lastInterval['A'])
# print('new interval for skazat', skazat.lastInterval['A'])
# print('new due date for byt:',byt.get_dueDate('A'))
# print('new due date for skazat:',skazat.get_dueDate('A'))
#
# print(delimiter)
# print('resetting user A')
# byt.addUser('A',overwrite=True)
# skazat.addUser('A',overwrite=True)
# byt.easinessFactor['A'] = 1.3
# skazat.easinessFactor['A'] = 1.3
# print('set last interval to 5 days')
# byt.lastInterval['A'] = 5
# byt.set_dueDate('A')
# skazat.lastInterval['A'] = 5
# skazat.set_dueDate('A')
# print('user A scores 85 on tests')
# byt.update_study_interval('A',.85)
# skazat.update_study_interval('A',.85)
# print('new interval for byt', byt.lastInterval['A'])
# print('new interval for skazat', skazat.lastInterval['A'])
# print('new due date for byt:',byt.get_dueDate('A'))
# print('new due date for skazat:',skazat.get_dueDate('A'))
#
# print(delimiter)
# print('resetting user A')
# byt.addUser('A',overwrite=True)
# skazat.addUser('A',overwrite=True)
# byt.easinessFactor['A'] = 1.3
# skazat.easinessFactor['A'] = 1.3
# print('set last interval to 6 days')
# byt.lastInterval['A'] = 6
# byt.set_dueDate('A')
# skazat.lastInterval['A'] = 6
# skazat.set_dueDate('A')
# print('user A scores 85 on tests')
# byt.update_study_interval('A',.85)
# skazat.update_study_interval('A',.85)
# print('new interval for byt', byt.lastInterval['A'])
# print('new interval for skazat', skazat.lastInterval['A'])
# print('new due date for byt:',byt.get_dueDate('A'))
# print('new due date for skazat:',skazat.get_dueDate('A'))
#
# print(delimiter)
# print('resetting user A')
# byt.addUser('A',overwrite=True)
# skazat.addUser('A',overwrite=True)
# byt.easinessFactor['A'] = 1.3
# skazat.easinessFactor['A'] = 1.3
# print('set last interval to 7 days')
# byt.lastInterval['A'] = 7
# byt.set_dueDate('A')
# skazat.lastInterval['A'] = 7
# skazat.set_dueDate('A')
# print('user A scores 85 on tests')
# byt.update_study_interval('A',.85)
# skazat.update_study_interval('A',.85)
# print('new interval for byt', byt.lastInterval['A'])
# print('new interval for skazat', skazat.lastInterval['A'])
# print('new due date for byt:',byt.get_dueDate('A'))
# print('new due date for skazat:',skazat.get_dueDate('A'))
#
# print(delimiter)
# print(delimiter)
# print('INCREASE LAST INTERVAL WHILE KEEPING EASINESS FACTOR CONSTANT - HIGH STARTING EASINESS FACTOR')
#
# print(delimiter)
# print('resetting user A')
# byt.addUser('A',overwrite=True)
# skazat.addUser('A',overwrite=True)
# byt.easinessFactor['A'] = 2.9
# skazat.easinessFactor['A'] = 2.9
# print('set last interval to 2 days')
# byt.lastInterval['A'] = 2
# byt.set_dueDate('A')
# skazat.lastInterval['A'] = 2
# skazat.set_dueDate('A')
# print('user A scores 85 on tests')
# byt.update_study_interval('A',.85)
# skazat.update_study_interval('A',.85)
# print('new interval for byt', byt.lastInterval['A'])
# print('new interval for skazat', skazat.lastInterval['A'])
# print('new due date for byt:',byt.get_dueDate('A'))
# print('new due date for skazat:',skazat.get_dueDate('A'))
#
# print(delimiter)
# print('resetting user A')
# byt.addUser('A',overwrite=True)
# skazat.addUser('A',overwrite=True)
# byt.easinessFactor['A'] = 2.9
# skazat.easinessFactor['A'] = 2.9
# print('set last interval to 3 days')
# byt.lastInterval['A'] = 3
# byt.set_dueDate('A')
# skazat.lastInterval['A'] = 3
# skazat.set_dueDate('A')
# print('user A scores 85 on tests')
# byt.update_study_interval('A',.85)
# skazat.update_study_interval('A',.85)
# print('new interval for byt', byt.lastInterval['A'])
# print('new interval for skazat', skazat.lastInterval['A'])
# print('new due date for byt:',byt.get_dueDate('A'))
# print('new due date for skazat:',skazat.get_dueDate('A'))
#
# print(delimiter)
# print('resetting user A')
# byt.addUser('A',overwrite=True)
# skazat.addUser('A',overwrite=True)
# byt.easinessFactor['A'] = 2.9
# skazat.easinessFactor['A'] = 2.9
# print('set last interval to 4 days')
# byt.lastInterval['A'] = 4
# byt.set_dueDate('A')
# skazat.lastInterval['A'] = 4
# skazat.set_dueDate('A')
# print('user A scores 85 on tests')
# byt.update_study_interval('A',.85)
# skazat.update_study_interval('A',.85)
# print('new interval for byt', byt.lastInterval['A'])
# print('new interval for skazat', skazat.lastInterval['A'])
# print('new due date for byt:',byt.get_dueDate('A'))
# print('new due date for skazat:',skazat.get_dueDate('A'))
#
# print(delimiter)
# print('resetting user A')
# byt.addUser('A',overwrite=True)
# skazat.addUser('A',overwrite=True)
# byt.easinessFactor['A'] = 2.9
# skazat.easinessFactor['A'] = 2.9
# print('set last interval to 5 days')
# byt.lastInterval['A'] = 5
# byt.set_dueDate('A')
# skazat.lastInterval['A'] = 5
# skazat.set_dueDate('A')
# print('user A scores 85 on tests')
# byt.update_study_interval('A',.85)
# skazat.update_study_interval('A',.85)
# print('new interval for byt', byt.lastInterval['A'])
# print('new interval for skazat', skazat.lastInterval['A'])
# print('new due date for byt:',byt.get_dueDate('A'))
# print('new due date for skazat:',skazat.get_dueDate('A'))
#
# print(delimiter)
# print('resetting user A')
# byt.addUser('A',overwrite=True)
# skazat.addUser('A',overwrite=True)
# byt.easinessFactor['A'] = 2.9
# skazat.easinessFactor['A'] = 2.9
# print('set last interval to 6 days')
# byt.lastInterval['A'] = 6
# byt.set_dueDate('A')
# skazat.lastInterval['A'] = 6
# skazat.set_dueDate('A')
# print('user A scores 85 on tests')
# byt.update_study_interval('A',.85)
# skazat.update_study_interval('A',.85)
# print('new interval for byt', byt.lastInterval['A'])
# print('new interval for skazat', skazat.lastInterval['A'])
# print('new due date for byt:',byt.get_dueDate('A'))
# print('new due date for skazat:',skazat.get_dueDate('A'))
#
# print(delimiter)
# print('resetting user A')
# byt.addUser('A',overwrite=True)
# skazat.addUser('A',overwrite=True)
# byt.easinessFactor['A'] = 2.9
# skazat.easinessFactor['A'] = 2.9
# print('set last interval to 7 days')
# byt.lastInterval['A'] = 7
# byt.set_dueDate('A')
# skazat.lastInterval['A'] = 7
# skazat.set_dueDate('A')
# print('user A scores 85 on tests')
# byt.update_study_interval('A',.85)
# skazat.update_study_interval('A',.85)
# print('new interval for byt', byt.lastInterval['A'])
# print('new interval for skazat', skazat.lastInterval['A'])
# print('new due date for byt:',byt.get_dueDate('A'))
# print('new due date for skazat:',skazat.get_dueDate('A'))

fileList = os.listdir('./verbs')
fileList.sort()
if 'verbsDB' not in fileList:
    for file in fileList:
        if file[-4:] == '.txt':
           with shelve.open('./verbs/verbsDB') as verbShelf:
               currentVerb = verb(file)
               verbShelf[file[:-4]] = currentVerb
    with shelve.open('./verbs/verbsDB') as verbShelf:
        verbShelf['users'] = []
