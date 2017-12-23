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
    def was_previouslyStudied(self, user):
        """returns the value of self.previouslyStudied for the user specified; used to determine whether a user should be presented with familiarization
        screens prior to quiz initiation"""
        return self.previouslyStudied[user]
    def addUser(self, user):
        """adds a user to the dictionaries used for the spaced repetition algorithm and preloads default values in these dictionaries"""
        self.easinessFactor[user] = 2.5
        self.lastInterval[user] = 1
        self.previouslyStudied [user] = False
    def update_study_interval(self, user, score):
        """user - a string of the name of the user whose interval is to be updated; score - a number between 0 and 1 representing performance on quiz;
        updates the desired study interval for the user (self.easinessFactor and self.lastInterval) using the SM2 algorithm"""
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
    def set_dateLastStudied(self):
        self.dateLastStudied = datetime.date.today()
    def is_overdue(self, user):
        #need to write some code to compare date last studied with interval
        pass


fileList = os.listdir('./verbs')
fileList.sort()

#for file in fileList:
#    if file[-4:] == '.txt':
#        with shelve.open('./verbs/verbsDB') as verbShelf:
#            verbShelf[file:-4] = verb(file)
