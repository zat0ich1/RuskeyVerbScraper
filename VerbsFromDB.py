#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 10:27:24 2017

@author: eli
"""

import os
import sqlite3
import datetime
import random
from PyQt4 import QtCore


def get_infinitive(infinitive):
    """infinitive - a string containing the transliterated version of the verb whose russian infinitive you wish to retrieve;
    returns the Russian form of the infinitive"""
    conn = sqlite3.connect('./verbsSQLDB')
    cursor = conn.cursor()
    cursor.execute('SELECT infinitive FROM verbCards WHERE transInfinitive=?',(infinitive,))
    result = cursor.fetchone()
    result = result[0]
    cursor.close()
    conn.close()
    return result

def get_aspect(infinitive):
    """infinitive - a string containing the transliterated version of the verb whose aspect you wish to retrieve;
    returns the aspect of the Russian verb"""
    conn = sqlite3.connect('./verbsSQLDB')
    cursor = conn.cursor()
    cursor.execute('SELECT aspect FROM verbCards WHERE transInfinitive=?',(infinitive,))
    result = cursor.fetchone()
    result = result[0]
    cursor.close()
    conn.close()
    return result


def get_frequencyRank(infinitive):
    """infinitive - a string containing the transliterated version of the verb whose frequency rank you wish to retrieve;
    returns the frequency rank of the verb"""
    conn = sqlite3.connect('./verbsSQLDB')
    cursor = conn.cursor()
    cursor.execute('SELECT frequency FROM verbCards WHERE transInfinitive=?',(infinitive,))
    result = cursor.fetchone()
    result = result[0]
    cursor.close()
    conn.close()
    return result

def get_meaning(infinitive):
    """infinitive - a string containing the transliterated version of the verb whose meaning you wish to retrieve;
    returns the meaning of the verb"""
    conn = sqlite3.connect('./verbsSQLDB')
    cursor = conn.cursor()
    cursor.execute('SELECT meaning FROM verbCards WHERE transInfinitive=?',(infinitive,))
    result = cursor.fetchone()
    result = result[0]
    cursor.close()
    conn.close()
    return result

def get_indicativeFirstSg(infinitive):
    """infinitive - a string containing the transliterated version of the verb whose indicative first person singular form you wish to retrieve;
    returns the indicative first person singular form of the verb"""
    conn = sqlite3.connect('./verbsSQLDB')
    cursor = conn.cursor()
    cursor.execute('SELECT firstSg FROM verbCards WHERE transInfinitive=?',(infinitive,))
    result = cursor.fetchone()
    result = result[0]
    cursor.close()
    conn.close()
    return result

def get_indicativeSecondSg(infinitive):
    """infinitive - a string containing the transliterated version of the verb whose indicative second person singular form you wish to retrieve;
    returns the indicative second person singular form of the verb"""
    conn = sqlite3.connect('./verbsSQLDB')
    cursor = conn.cursor()
    cursor.execute('SELECT secondSg FROM verbCards WHERE transInfinitive=?',(infinitive,))
    result = cursor.fetchone()
    result = result[0]
    cursor.close()
    conn.close()
    return result

print(get_indicativeSecondSg('khotjet'))
#     """returns a string containing the non-past indicative 2nd person singular form of the verb"""
#     return self.indicativeSecondSg
# def get_indicativeThirdSg(self):
#     """returns a string containing the non-past indicative 3rd person singular form of the verb"""
#     return self.indicativeThirdSg
# def get_indicativeFirstPl(self):
#     """returns a string containing the non-past indicative 1st person plural form of the verb"""
#     return self.indicativeFirstPl
# def get_indicativeSecondPl(self):
#     """returns a string containing the non-past indicative 2nd person plural form of the verb"""
#     return self.indicativeSecondPl
# def get_indicativeThirdPl(self):
#     """returns a string containing the non-past indicative 3rd person plural form of the verb"""
#     return self.indicativeThirdPl
# def get_imperativeSg(self):
#     """returns a string containing the imperative singular form of the verb"""
#     return self.imperativeSg
# def get_imperativePl(self):
#     """returns a string containing the imperative plural form of the verb"""
#     return self.imperativePl
# def get_pastMasc(self):
#     """returns a string containing the past masculine form of the verb"""
#     return self.pastMasc
# def get_pastFem(self):
#     """returns a string containing the past feminine form of the verb"""
#     return self.pastFem
# def get_pastNeut(self):
#     """returns a string containing the past neuter form of the verb"""
#     return self.pastNeut
# def get_pastPl(self):
#     """returns a string containing the past plural form of the verb"""
#     return self.pastPl
# def get_examplesList(self, stripPunctuation=False, toLower=False):
#     """takes an optional parameter to strip punctuation marks; returns a list of the russian example sentences; the indices for these match the indices in the corresponding translation list"""
#     if not stripPunctuation and not toLower:
#         return self.examplesList
#     else:
#
#         strippedList = self.examplesList[:]
#         if stripPunctuation:
#             for i in range(len(strippedList)):
#                 strippedList[i] = strippedList[i].replace(',','')
#                 strippedList[i] = strippedList[i].replace('.','')
#                 strippedList[i] = strippedList[i].replace(':','')
#                 strippedList[i] = strippedList[i].replace(';','')
#                 strippedList[i] = strippedList[i].replace('?','')
#                 strippedList[i] = strippedList[i].replace('!','')
#         if toLower:
#             for i in range(len(strippedList)):
#                 strippedList[i] = strippedList[i].lower()
#         return strippedList
# def get_verbForList(self):
#     """returns a string consisting of the z-filled frequency rank, a space, and the infinitive form"""
#     freqstr = self.frequencyRank.zfill(4) + " "
#     return freqstr + self.infinitive
# def get_numExamples(self):
#     """returns the number of examples for a given verb"""
#     return len(self.examplesList)
# def get_examplesListTranslations(self):
#     """returns a list of translations of the russian example sentences; the indices for these match the indices in the corresponding examples list"""
#     return self.examplesListTranslations
# def get_verbAudioList(self):
#     """returns a list of the audio file names for the verb. The indices should match the example sentence list indices, excepting the final item, which is the audio for the conjugation"""
#     return self.verbAudioList
# def get_conjugationAudio(self):
#     """returns the name of the conjugation audio file"""
#     return self.verbAudioList[-1]
# def get_randomizedExamplesList(self):
#     """returns a list of randomized example sentences; each member of the list is a list of the words in the example in random order\n
#     e.g. the example sentence 'Я была с ним честной' becomes ['Я', 'с', 'была', 'ним', 'честной'] (this list would be an element of the list returned)"""
#     randomizedExamples = []
#     for string in self.examplesList:
#         string = string.replace(',','')
#         string = string.replace('.','')
#         string = string.replace(':','')
#         string = string.replace(';','')
#         string = string.replace('?','')
#         string = string.replace('!','')
#         sentenceList = string.split(' ')
#         random.shuffle(sentenceList)
#         randomizedExamples.append(sentenceList)
#     return randomizedExamples
# def addUser(self, user, overwrite=False):
#     """user - user to be added; overwrite - optional parameter (False by default) - if set to true, will reset SM2 values for given user name if that user already exists;
#     otherwise, if the specified user is not already loaded, adds a user to the dictionaries used for the spaced repetition algorithm and preloads default values in these dictionaries"""
#     if not overwrite:
#         if user not in self.users:
#             self.users.append(user)
#             self.easinessFactor[user] = 2.5
#             self.lastInterval[user] = 1
#             self.previouslyStudied [user] = False
#             self.dateLastStudied[user] = QtCore.QDate.currentDate()
#             self.dueDate[user] = self.dateLastStudied[user].addDays(self.lastInterval[user])
#     else:
#         if user not in self.users:
#             self.users.append(user)
#         self.easinessFactor[user] = 2.5
#         self.lastInterval[user] = 1
#         self.previouslyStudied [user] = False
#         self.dateLastStudied[user] = QtCore.QDate.currentDate()
#         self.dueDate[user] = self.dateLastStudied[user].addDays(self.lastInterval[user])
#
# def was_previouslyStudied(self, user):
#     """returns the value of self.previouslyStudied for the user specified; used to determine whether a user should be presented with familiarization
#     screens prior to quiz initiation"""
#     return self.previouslyStudied.get(user, False)
# def was_studiedToday(self,user):
#     """returns True if a user last studied a verb today; False otherwise"""
#     if not self.was_previouslyStudied(user):
#         return False
#     elif self.was_previouslyStudied(user) and self.dateLastStudied[user] == QtCore.QDate.currentDate():
#         return True
#     else:
#         return False
# def update_study_interval(self, user, score):
#     """user - a string of the name of the user whose interval is to be updated; score - a number between 0 and 1 representing performance on quiz;
#     updates the desired study interval for the user (self.easinessFactor and self.lastInterval) using the SM2 algorithm"""
#
#     if not self.was_studiedToday(user): #only update interval per SM2 algorithm if this is the first time the user is studying the verb today
#         self.previouslyStudied[user] = True
#         self.set_dateLastStudied(user)
#         if (score*5) < 3.5:
#             self.lastInterval[user] = 1
#         else:
#             if self.lastInterval.get(user, 1) == 1:
#                 print('user interval is 1; setting to 2')
#                 self.lastInterval[user] = 2
#                 print(self.lastInterval[user])
#             elif self.lastInterval[user] == 2:
#                 print('user interval is 2; setting to 4')
#                 self.lastInterval[user] = 4
#                 print(self.lastInterval[user])
#             else:
#                 print('user interval was greater than 2; using sm2 algorimthm')
#                 print('prior easiness factor:',self.easinessFactor[user])
#                 self.easinessFactor[user] += (0.1-(5-(score*5))*(0.08+(5-(score*5))*0.02))
#                 if self.easinessFactor[user] < 1.3:
#                     self.easinessFactor[user] = 1.3
#                 print('new easiness factor:',self.easinessFactor[user])
#                 print('old interval:',self.lastInterval[user])
#                 self.lastInterval[user] *= self.easinessFactor[user]
#                 self.lastInterval[user] = int(self.lastInterval[user])
#                 print('new interval:',self.lastInterval[user])
#         self.dueDate[user] = self.dateLastStudied[user].addDays(self.lastInterval[user])
#     else: #if the user studies the verb for a second or greater time and scores 0.7 or above, simply add one to the due date - this will prevent the
#     # user from studying a verb a ton of times in one day to dramatically increase the study interval
#         self.previouslyStudied[user] = True
#         self.set_dateLastStudied(user)
#         if (score*5) < 3.5:
#             self.lastInterval[user] = 1
#         else:
#             self.lastInterval[user] += 1
#             self.dueDate[user] = self.dateLastStudied[user].addDays(self.lastInterval[user])
# def set_dateLastStudied(self, user, date=QtCore.QDate.currentDate()):
#     """user - the user whose date last studied you want to set; date - QDate object - defaults to current date;
#     updates dateLastStudied for the specified user to the specified date"""
#     self.dateLastStudied[user] = date
# def get_dateLastStudied(self, user):
#     """user - the user whose dateLastStudied you wish to retrieve; returns a Qstring of the date last studied"""
#     dateRequested = self.dateLastStudied.get(user, QtCore.QDate.currentDate())
#     return dateRequested.toString('MM.dd.yyyy')
# def get_nextStudyDateDisplay(self,user):
#     """returns a string indicating the status of a current verb for a given user;
#     if the verb is overdue, returns "# days overdue" where # is the days overdue;
#     if the user has not yet studied a verb returns the phrase 'Not yet studied';
#     if the verb is due on the day it is being viewed, returns 'Due today!';
#     if the verb has been studied but is not yet due, returns the due date in mm.dd.yyyy format"""
#     if not self.was_previouslyStudied(user):
#         return "Not yet studied"
#     else:
#         if self.is_overdue(user):
#             return str(self.get_daysOverdue(user)) + " days overdue"
#         else:
#             displayDate = self.dueDate[user]
#             if displayDate == QtCore.QDate.currentDate():
#                 return("Due today!")
#             return displayDate.toString('MM.dd.yyyy')
# def is_overdue(self, user):
#     """returns True if a verb is overdue; False otherwise"""
#     if not self.was_previouslyStudied(user):
#         return False
#     elif self.get_daysOverdue(user) > 0:
#         return True
#     else:
#         return False
# def get_daysOverdue(self,user):
#     """returns the difference between today's date and the next study date"""
#     return self.dueDate[user].daysTo(QtCore.QDate.currentDate())
# def get_dueDate(self,user,stringFormat=True):
#     """returns a the due date for a verb for the given user in Qstring mm.dd.yyyy format"""
#     return self.dueDate[user].toString('MM.dd.yyyy')
# def set_dueDate(self,user):
#     self.dueDate[user] = self.dateLastStudied[user].addDays(self.lastInterval[user])
