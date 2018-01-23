import sys
import os
import shelve
import random
from fuzzywuzzy import fuzz
from playsound import playsound
from ShelveVerbs import verb
from PyQt4 import QtGui
from PyQt4 import QtCore

with shelve.open('./verbs/verbsDB') as verbShelf:
    temp = verbShelf['users']
    temp.append('Dave')
    temp.append('Jill')
    verbShelf['users'] = temp
    verbShelf['0001byt'].addUser('Dave')
    verbShelf['0003moch'].addUser('Dave')
    verbShelf['0006stat'].addUser('Dave')
    verbShelf('0010idti').addUser('Dave')
    verbShelf['0001byt'].addUser('Jill')
    verbShelf['0005govorit'].addUser('Jill')
    verbShelf['0008khotjet'].addUser('Jill')
    verbShelf['0010idti'].addUser('Jill')
    fiveDaysAgo = QtCore.QDate.currentDate().addDays(-5)
    sevenDaysAgo = QtCore.QDate.currentDate().addDays(-7)
    elevenDaysAgo = QtCore.QDate.currentDate().addDays(-11)
    eightDaysFromNow = QtCore.QDate.currentDate().addDays(8)
    fourDaysFromNow = QtCore.QDate.currentDate().addDays(4)
    elevenDaysFromNow = QtCore.QDate.currentDate().addDays(11)
    verbShelf['0001byt'].set_dateLastStudied('Dave', fiveDaysAgo)
    verbShelf['0003moch'].set_dateLastStudied('Dave', fiveDaysAgo)
    verbShelf['0006stat'].set_dateLastStudied('Dave', sevenDaysAgo)
    verbShelf['0010idti'].set_dateLastStudied('Dave', eightDaysFromNow)
