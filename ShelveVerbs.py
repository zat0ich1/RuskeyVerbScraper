#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 10:27:24 2017

@author: eli
"""

import os
import shelve


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
    #need to write get methods and implement spaced rep algorithm

fileList = os.listdir('./verbs')
fileList.sort()

#for file in fileList:
#    if file[-4:] == '.txt':
#        with shelve.open('./verbs/verbsDB') as verbShelf:
#            verbShelf[file:-4] = verb(file)