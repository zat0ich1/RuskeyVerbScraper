#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 11:42:13 2017

@author: eli
"""

import datetime

class someObj(object):
    def __init__(self, easinessFactor, lastInterval):
        self.easinessFactor = easinessFactor
        self.lastInterval = lastInterval
    def getNextInterval(self, score):
        if (score*5) < 3.5:
            self.lastInterval = 1
        else:
            if self.lastInterval == 1:
                self.lastInterval = 2
            elif self.lastInterval == 2:
                self.lastInterval = 6
            else:
                self.easinessFactor += (0.1-(5-(score*5))*(0.08+(5-(score*5))*0.02))
                if self.easinessFactor < 1.3:
                    self.easinessFactor = 1.3
                elif self.easinessFactor > 5:
                    self.easinessFactor = 5
                self.lastInterval *= self.easinessFactor
        print('new interval: ',self.lastInterval)

#def CalculateEasinessFactor(oldFactor, score):
#    score *= 100
#    newFactor = oldFactor + 0.1-(100-score)*(0.02+(100-score)*0.02)
#    if newFactor < 1.3:
#        return 1.3
#    return newFactor
#
#
#easiness = 2.5
#
#def getNextReviewDate(n, score, lastInterval, easinessFacor):
#    if n == 1:
#        return 1
#    elif n == 2:
#        return 3
#    else:
#        return lastInterval*CalculateEasinessFactor(easinessFactor,score)
#
#
#score = 1.0
#thisList = []
#
#for i in range (1,10):
#    if i != 1:
#        easiness = CalculateEasinessFactor(easiness,score)
#    thisList.append(getNextReviewDate(i,score))
#scores = [0.9,0.8,0.7,0.6,0.8,0.7]
#test1 = someObj(2.5,1)
#for i in scores:
#    test1.getNextInterval(i)
test1 = someObj(2.5,1)
for i in range(10):
    test1.getNextInterval(0.9)
