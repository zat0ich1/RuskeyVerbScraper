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

def listAverage(someList, returninteger=False):
    """takes a list of numbers and an optional parameter to return an integer
    value; returns an average of the values in the list"""
    mySum = 0
    for i in range(len(someList)):
        mySum += someList[i][0]
    myLen = len(someList)
    if returninteger:
        return int(mySum/myLen)
    else:
        return round(mySum/myLen,2)

def get_daysOverdue(verb, user):
    """verb - transliterated form of a russian infinitive (string);
    user - name of user (string); returns the number of days a verb is
    overdue for a given user"""
    conn = sqlite3.connect('./verbsSQLDB')
    cursor = conn.cursor()
    cursor.execute("""SELECT dueDate FROM userAverage INNER JOIN verbCards
                   ON userAverage.verbID = verbCards.verbID
                   WHERE verbCards.transInfinitive=? AND userAverage.userName=?
                   """, (verb, user))
    verbDueDate = cursor.fetchall()
    cursor.close()
    conn.close()
    verbDueDate = verbDueDate[0][0]
    verbDueDate = QtCore.QDate.fromString(verbDueDate, QtCore.Qt.ISODate)
    return verbDueDate.daysTo(QtCore.QDate.currentDate())


def get_formsList(verb):
    """verb - transliterated form of a russian infinitive (string);
    returns a list of the forms (used to populate the verb browser)
    """
    conn = sqlite3.connect('./verbsSQLDB')
    cursor = conn.cursor()
    cursor.execute("""SELECT
                   infinitive,
                   meaning,
                   aspect,
                   frequency,
                   firstSg,
                   secondSg,
                   thirdSg,
                   firstPl,
                   secondPl,
                   thirdPl,
                   imperativeSg,
                   imperativePl,
                   pastMasc,
                   pastFem,
                   pastNeut,
                   pastPl
                   FROM verbCards WHERE transInfinitive=?""",
                   (verb,))
    forms = cursor.fetchall()
    cursor.close()
    conn.close()
    formsList = []
    for i in forms[0]:
        formsList.append(str(i))
    return formsList

def get_userList():
    """returns a list of the users in verbsSQLDB"""
    conn = sqlite3.connect('./verbsSQLDB')
    cursor = conn.cursor()
    cursor.execute("""SELECT DISTINCT userName FROM userAverage
                   ORDER BY userName ASC""")
    result = []
    for i in cursor.fetchall():
        print(i[0])
        result.append(i[0])
    cursor.close()
    conn.close()
    return result

def userExists(name):
    """returns true if a user is in the user DB; false otherwise"""
    conn = sqlite3.connect('./verbsSQLDB')
    cursor = conn.cursor()
    cursor.execute("""SELECT userName FROM userAverage WHERE userName=?""",
                   (name,))
    result = cursor.fetchall()
    if result == []:
        return False
    else:
        return True


def get_dueDateText(verb, user):
    """verb - transliterated Russian infinitive (string); user - user name (string);
    returns a string indicating the status of a current verb for a given user;
    if the verb is overdue, returns "# days overdue" where # is the days overdue;
    if the user has not yet studied a verb returns the phrase 'Not yet studied';
    if the verb is due on the day it is being viewed, returns 'Due today!';
    if the verb has been studied but is not yet due, returns the due date
    in ISO date format"""
    daysOverdue = get_daysOverdue(verb,user)
    conn = sqlite3.connect('./verbsSQLDB')
    cursor = conn.cursor()
    cursor.execute("""SELECT previouslyStudied, dueDate FROM userAverage
                   INNER JOIN verbCards
                   ON verbCards.verbID = userAverage.verbID
                   WHERE transInfinitive=? AND userName=?""",
                   (verb, user))
    result = cursor.fetchall()
    previouslyStudied = result[0][0]
    dueDate = result[0][1]
    if previouslyStudied == 0:
        return "Not studied yet"
    else:
        if daysOverdue > 0:
            return str(daysOverdue) + " days overdue"
        if daysOverdue == 0:
            return "Due today!"
        else:
            return dueDate

def populate_average(verb, user):
    """verb - transliterated version of a russian infinitive or the verbID of a
    Russian verb; user - the name of a user in the users DB; calculates the
    average scores for all examples linked with a given verb and stores it in
    the userAverage table; this data will be used to determine the display
    order of verbs and to provide the user with a sense of how overdue
    something is."""
    conn = sqlite3.connect('./verbsSQLDB')
    cursor = conn.cursor()
    cursor.execute('SELECT userName FROM users WHERE username=?',(user,))
    testForUser = cursor.fetchall()
    if type(verb) == int:
        targetID = verb
    if type(verb) != int:
        cursor.execute('SELECT verbID FROM verbCards WHERE transInfinitive=?',
                       (verb,))
        targetID = cursor.fetchone()
        targetID = targetID[0]
    cursor.execute('SELECT verbID FROM userAverage WHERE verbID=? AND userName=?',
                   (targetID, user))
    testForVerb = cursor.fetchall()
    if testForUser != []:
        cursor.execute('SELECT easinessFactor FROM users where verbID=?',
                       (targetID,))
        easinessList = cursor.fetchall()

        easinessAverage = listAverage(easinessList)
        cursor.execute('SELECT lastInterval FROM users where verbID=?',
                       (targetID,))
        intervalList = cursor.fetchall()
        intervalAverage = listAverage(intervalList, returninteger=True)
        cursor.execute("""SELECT dateLastStudied FROM users
                       ORDER BY dateLastStudied ASC""")
        earliestDate = cursor.fetchone()
        earliestDate = earliestDate[0]
        cursor.execute('SELECT dueDate FROM users ORDER BY dueDate ASC')
        earliestDueDate = cursor.fetchone()
        earliestDueDate = earliestDueDate[0]
        if testForVerb == []:
            cursor.execute("""INSERT INTO userAverage VALUES
                           (?, ?, ?, ?, ?, ?, ?)""",
                           (user, targetID, easinessAverage, intervalAverage,
                            earliestDate, earliestDueDate, False))
        else:
            cursor.execute("""SELECT dueDate FROM userAverage
                           INNER JOIN verbCards ON
                           userAverage.verbID = verbCards.verbID
                           WHERE userAverage.userName=?
                           AND verbCards.transInfinitive=?""",
                           (user, verb))
            dueDate = cursor.fetchall()
            dueDate = dueDate[0][0]
            dueDate = QtCore.QDate.fromString(dueDate, QtCore.Qt.ISODate)
            cursor.execute("""UPDATE userAverage SET easinessFactor=?,
                           lastInterval=?, dateLastStudied=?, dueDate=?,
                           previouslyStudied=? WHERE userName=?
                           AND verbID=?""",
                           (easinessAverage, intervalAverage, earliestDate,
                            earliestDueDate, True, user, targetID))
        conn.commit()
    cursor.close()
    conn.close()

def add_user(name):
    """adds a user to the users table and populates default values for each
    example in the following columns: easiness factor (2.5), last interval (1);
    previously studied (false); date last studied (today); due date (date last
    studied + last interval)"""
    conn = sqlite3.connect('./verbsSQLDB')
    cursor = conn.cursor()
    cursor.execute('SELECT userName FROM users WHERE userName=?',(name,)) #check
    testForUser = cursor.fetchall() #if user is already in DB
    if testForUser == []:
        cursor.execute('SELECT exampleID, verbID FROM examples')
        dateLastStudied = QtCore.QDate.currentDate().toString(QtCore.Qt.ISODate)
        lastInterval = 1
        easinessFactor = 2.5
        previouslyStudied = False
        dueDate = QtCore.QDate.currentDate().addDays(1).toString(QtCore.Qt.ISODate)
        for i in cursor.fetchall():
            cursor.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)',
                           (name, int(i[0]), int(i[1]), easinessFactor, lastInterval,
                            dateLastStudied,  dueDate))
        cursor.execute('SELECT verbID FROM verbCards')
        allVerbs = cursor.fetchall() #get a list of tuples; each tuple has only
        conn.commit()
    cursor.close()
    conn.close()
    if testForUser == []:
        for someVerb in allVerbs: #the verbID
            someVerbID = someVerb[0] #extract verbID from tuples
            populate_average(someVerbID, name)

def del_user(name):
    """removes a user from the user table"""
    conn = sqlite3.connect('./verbsSQLDB')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE userName=?',(name,))
    cursor.execute('DELETE FROM userAverage WHERE userName=?',(name,))
    conn.commit()
    cursor.close()
    conn.close()

def get_SortedVerbList(user):
    """returns a list of available verbs for the given user; verbs which have
    previously been studied are sorted at the front of the list by days overdue;
    other verbs are sorted by frequency rank"""
    previouslyStudiedList = []
    notPreviouslyStudiedList = []
    conn = sqlite3.connect('./verbsSQLDB')
    cursor = conn.cursor()
    cursor.execute("""SELECT frequency, infinitive FROM verbCards
                   INNER JOIN userAverage ON verbCards.verbID = userAverage.verbID
                   WHERE userName=? AND previouslyStudied=?
                   ORDER BY dueDate ASC""",
                   (user, 1)) #need to add days overdue to userAverage table

    for i in cursor.fetchall():
        freq = str(i[0]).zfill(4) + ' '
        previouslyStudiedList.append(freq + i[1])
    cursor.execute("""SELECT frequency, infinitive FROM verbCards
                   INNER JOIN userAverage ON verbCards.verbID = userAverage.verbID
                   WHERE userName=? AND previouslyStudied=?
                   ORDER BY frequency ASC""",
                   (user, 0))
    for i in cursor.fetchall():
        freq = str(i[0]).zfill(4) + ' '
        notPreviouslyStudiedList.append(freq + i[1])
    return previouslyStudiedList + notPreviouslyStudiedList

# populate_average('byt', 'Steve')

# add_user('Steve')
# add_user('Jim')
# print(get_userlist())


# def get_conjugation(verb):
#     """verb - the transliterated string version of a russian infinitive; returns
#     a list that is used to populate the verb browser interface with forms;
#     the list has the following: [0] infinitive, [1] meaning, [2] aspect,
#     [3] fequency, [4] indicative first person singular,
#     [5]indicative second person singular, [6] indicative third person singular,
#     [7] indicative first person plural, [8] indicative second person plural,
#     [9] indicative third person plural, [10] imperative singular,
#     [11] imperative plural, [12] masculine past, [13] feminine past,
#     [14] neuter past, [15] plural past, [16] due date (if previously studied)
#     or "not previously studied""""
#     conn = sqlite3.connect('./verbsSQLDB')
#     cursor = conn.cursor()
#     cursor.execute("""SELECT infinitive, meaning, aspect, frequency, firstSg,
#                    secondSg, thirdSg, firstPl, secondPl, thirdPl, imperativeSg,
#                    imperativePl, pastMasc, pastFem, pastNeut, pastPl,  WHERE
#                    transInfinitive=?""", (verb,))
#     result = cursor.fetchall()
#     cursor.execute("""SELECT""") #need to create new table to store average
#     #values for verb card due dates


def get_infinitive(infinitive):
    """infinitive - a string containing the transliterated version of the verb
    whose russian infinitive you wish to retrieve; returns the Russian form of
    the infinitive"""
    conn = sqlite3.connect('./verbsSQLDB')
    cursor = conn.cursor()
    cursor.execute('SELECT infinitive FROM verbCards WHERE transInfinitive=?',
                   (infinitive,))
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
