#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 10:27:24 2017

@author: eli
"""

import os
import shelve
import datetime


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
            self.easinessFactor = 2.5 # these will be used with SM2 algorithm to
            self.lastInterval = 1     # find out when the object should next be studied
            self.dateLastStudied = None # will be updated when first studied
            
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
        return self.infinitive
    def get_aspect(self):
        return self.aspect
    def get_frequencyRank(self):
        return self.frequencyRank
    def get_meaning(self):
        return self.meaning
    def get_indicativeFirstSg(self):
        return self.indicativeFirstSg
    def get_indicativeSecondSg(self):
        return self.indicativeSecondSg
    def get_indicativeThirdSg(self):
        return self.indicativeThirdSg
    def get_indicativeFirstPl(self):
        return self.indicativeFirstPl
    def get_indicativeSecondPl(self):
        return self.indicativeSecondPl
    def get_indicativeThirdPl(self):
        return self.indicativeThirdPl
    def get_pastMasc(self):
        return self.pastMasc
    def get_pastFem(self):
        return self.pastFem
    def get_pastNeut(self):
        return self.pastNeut
    def get_pastPl(self):
        return self.pastPl
    def get_examplesList(self):
        return self.examplesList
    def get_examplesListTranslations(self):
        return self.examplesListTranslations
    def get_verbAudioList(self):
        return self.verbAudioList
    
    def update_study_interval(self, score):
        """score - a number between 0 and 1 representing performance on quiz;
        updates the desired study interval (self.easinessFactor and self.lastInterval) using the SM2 algorithm"""
        if (score*5) < 3.5:
            self.lastInterval = 1
        else:
            if self.lastInterval == 1:
                self.lastInterval = 2
            elif self.lastInterval == 2:
                self.lastInterval = 4
            else:
                self.easinessFactor += (0.1-(5-(score*5))*(0.08+(5-(score*5))*0.02))
                if self.easinessFactor < 1.3:
                    self.easinessFactor = 1.3
                elif self.easinessFactor > 5:
                    self.easinessFactor = 5
                self.lastInterval *= self.easinessFactor
                self.lastInterval = int(self.lastInterval)
    def set_dateLastStudied(self):
        self.dateLastStudied = datetime.date.today()
        

fileList = os.listdir('./verbs')
fileList.sort()

#for file in fileList:
#    if file[-4:] == '.txt':
#        with shelve.open('./verbs/verbsDB') as verbShelf:
#            verbShelf[file:-4] = verb(file)