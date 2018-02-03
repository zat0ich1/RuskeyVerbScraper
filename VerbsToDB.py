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
                self.examplesList.append(
                    self.verbFileLinesList[i].replace(u'\n',''))
                self.examplesListTranslations.append(
                    self.verbFileLinesList[i+1].replace(u'\n',''))
            for i in range(len(self.examplesList)):
                audioFileName = ('./verbAudio/'
                                 + verbFileName[:-4]
                                 + str(i)
                                 + '.mp3')
                self.verbAudioList.append(audioFileName)
            self.verbAudioList.append('./verbAudio/'
                                      + verbFileName[:-4]+'.mp3')
            #append conjugation audio last so that indexes for examples line up

            self.transliterateDict = {'а':'a',
                                 'б':'b',
                                 'в':'v',
                                 'г':'g',
                                 'д':'d',
                                 'е':'je',
                                 'ё':'jo',
                                 'ж':'zh',
                                 'з':'z',
                                 'и':'i',
                                 'й':'j',
                                 'к':'k',
                                 'л':'l',
                                 'м':'m',
                                 'н':'n',
                                 'о':'o',
                                 'п':'p',
                                 'р':'r',
                                 'с':'s',
                                 'т':'t',
                                 'у':'u',
                                 'ф':'f',
                                 'х':'kh',
                                 'ц':'ts',
                                 'ч':'ch',
                                 'ш':'sh',
                                 'щ':'shch',
                                 'ъ':'',
                                 'ы':'y',
                                 'ь':'',
                                 'э':'e',
                                 'ю':'ju',
                                 'я':'ja',
                                 chr(769):''}
    def transliterate(self):
        """returns a transliterated version of the infitive form"""
        result = ""
        for letter in self.infinitive:
            result += self.transliterateDict.get(letter, letter)
        return result

    def writeVerb(self):
        self.conn = sqlite3.connect('./verbsSQLDB')
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS verbCards(verbID
                            INTEGER PRIMARY KEY, infinitive TEXT,
                            transInfinitive TEXT, aspect TEXT, frequency INT,
                            meaning TEXT, firstSg TEXT, secondSg TEXT,
                            thirdSg TEXT, firstPl TEXT, secondPl TEXT,
                            thirdPl TEXT, imperativeSg TEXT, imperativePl TEXT,
                            pastMasc TEXT, pastFem TEXT, pastNeut TEXT,
                            pastPl Text, conjAudio TEXT)""")
        self.cursor.execute("""INSERT INTO verbCards (infinitive,
                            transinfinitive, aspect, frequency, meaning,
                            firstSg, secondSg, thirdSg, firstPl, secondPl,
                            thirdPl, imperativeSg, imperativePl, pastMasc,
                            pastFem, pastNeut, pastPl, conjAudio) VALUES(?, ?,
                            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                            (self.infinitive, self.transliterate(), self.aspect,
                             self.frequencyRank, self.meaning,
                             self.indicativeFirstSg, self.indicativeSecondSg,
                             self.indicativeThirdSg, self.indicativeFirstPl,
                             self.indicativeSecondPl, self.indicativeThirdPl,
                             self.imperativeSg, self.imperativePl,
                             self.pastMasc, self.pastFem, self.pastNeut,
                             self.pastPl, self.verbAudioList[-1]))
        self.cursor.execute('SELECT verbID FROM verbCards WHERE infinitive=?',
                            (self.infinitive,))
        self.target = self.cursor.fetchone()
        self.target = self.target[0]
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS examples(
                            exampleID INTEGER PRIMARY KEY,
                            verbID REFERENCES verbCards(verbID),
                            example TEXT, translation TEXT,
                            exampleAudio TEXT)""")
        for i in range(len(self.examplesList)):
            self.cursor.execute("""INSERT INTO examples(verbID, example,
                                translation, exampleAudio) VALUES(?,?,?,?)""",
                                (self.target, self.examplesList[i],
                                 self.examplesListTranslations[i],
                                 self.verbAudioList[i]))
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(userName TEXT,
                            exampleID REFERENCES examples(exampleID),
                            verbID REFERENCES verbCards(verbID),
                            easinessFactor REAL, lastInterval INT,
                            dateLastStudied TEXT, dueDate TEXT)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS
                            userAverage(userName REFERENCES user(userName),
                            verbID REFERENCES verbCards(verbID),
                            easinessFactor REAL, lastInterval INT,
                            dateLastStudied TEXT, dueDate TEXT,
                            previouslyStudied BOOLEAN)""")
        self.conn.commit()
        self.cursor.close()
        self.conn.close()




fileList = os.listdir('./verbs')
fileList.sort()

if 'verbsSQLDB' not in fileList:
    for file in fileList:
        if file[-4:] == '.txt':
            currentVerb = verb(file)
            currentVerb.writeVerb()
