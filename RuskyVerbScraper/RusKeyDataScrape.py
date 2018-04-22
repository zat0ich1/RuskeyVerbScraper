# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import boto3
import os
baseUrl = 'https://en.openrussian.org'
url = 'https://en.openrussian.org/list/verbs'
verbMasterList = [] #this will be a master list containing
              #a list for each verb as its elements
verbFormsKey = ['infinitive','aspect','frequency','meaning','1st singular',
                '2nd singular', '3rd singular', '1st plural','2nd plural',
                '3rd plural', 'imperative singular','imperative plural',
                'past masculine', 'past feminine', 'past neuter', 'past plural'
                ] #this contains the name of each element appended for an individual verb
commonEndUnstressed = ["его",
                       "Его",
                       "она",
                       "Она",
                       "они",
                       "Они",
                       "себе",
                       "Себе",
                       "тебе",
                       "Тебе",
                       "меня",
                       "Меня",
                       "тебя",
                       "Тебя",
                       "себя",
                       "Себя",
                       "уже",
                       "Уже",
                       "чего",
                       "Чего",
                       "ничего",
                       "Ничего"] #list of words commonly left unstressed in examples that have stressed final vowels
transliterateDict = {'а':'a',
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

def padThousands(num):
    """num - a string representation of a number less than 1000; returns
    the string representation with leading 0s to the thousands place"""
    # 4 > 0004, 12 > 0012
    num = str(num)
    return num.zfill(4)


def countVowels(word):
    """takes a string and returns the number of Russian vowels"""
    #For use in checking whether a word has a stress
    count = 0
    for letter in word:
        if letter in "аеёиоуыэюяАЕЁИОУЫЭЮЯ":
            count += 1
    return count


def checkWordForStress(word):
    """takes a string and returns True if the word is one syllable long or has
    two or more syllables, one of which is accented; returns False otherwise"""
    #limitation here would be stressed prepositions...
    if countVowels(word) > 1 and chr(769) not in word and 'ё' not in word:
        return False
    return True

def checkSentenceForStress(sentence):
    """sentence - a string containing a russian sentence
    returns True if every word is properly stressed, false otherwise"""
    sentence = sentence.split(' ')
    for word in sentence:
        if not checkWordForStress(word):
            return False
    return True

def markSimpleStresses(sentence):
    """add stresses to short common russian words that are often unstressed
    sentence - a string of russian words; returns same string with unstressed common words replaced by stressed versions"""
    sentence = sentence.split(' ')
    for n in range(len(sentence)):
        if sentence[n] in commonEndUnstressed:
            sentence[n] += chr(769)
        elif sentence[n] == "больше":
            sentence[n] = "бо"+ chr(769) + "льше"
        elif sentence[n] == "нужно":
            sentence[n] = "ну" + chr(769) + "жно"
        elif sentence[n] == "будет":
            sentence[n] = "бу" + chr(769) + "дет"
        elif sentence[n] == "много":
            sentence[n] = "мно" + chr(769) + "го"
        elif sentence[n] == "Тома":
            sentence[n] = "То" + chr(769) + "ма"
        elif sentence[n] == "Томом":
            sentence[n] = "То" + chr(769) + "мом"
        result = " ".join(sentence)
    return result

def transliterate(word):
    """takes a russian string and returns the string transliterated into latin characters"""
    result = ""
    for letter in word:
        result += transliterateDict[letter]
    return result    

def stripSoupList(SoupObj, string=False):
    """takes a list generated from a Soup object and removes newlines and \xa0 
    characters. Returns either a list of stripped strings (default) or a string"""
    if string == True:
        holder = ''
        for item in SoupObj:
            holder += item.text
        holder = holder.replace(u'\xa0','')
        holder = holder.replace(u'\n','')
        return holder
    else:
        holder = []
        for item in SoupObj:
            holder.append(item.text)
        for i in range(len(holder)):
            holder[i] = holder[i].replace(u'\xa0','')
            holder[i] = holder[i].replace(u'\n','')
        return holder


def getExamples(someurl, verb):
    """takes url for a verb and the infinitive form for that verb; returns a list of properly stresed examples;
    if not enough properly stressed examples are located, asks the user to
    manually specify missing stresses for examples with least missing stresses
    """
    verbPage = requests.get(someurl)
    verbSoupObj = BeautifulSoup(verbPage.content, 'lxml') #creates a beautiful soup object from the verb's conjugation page
    russianExamplesIterable = verbSoupObj.find('ul', class_='sentences') #this element will be present if the verb has examples
    try:
        russianExamplesIterable = russianExamplesIterable.find_all('li') #find all the li elements in the examples list
        russianExamples = []
        for item in russianExamplesIterable:
            stringHolder = item.text #put the text into a holder string
            stringHolder = stringHolder.replace(u'\xa0','') #remove nonbreaking spaces
            stringHolder = stringHolder.replace(u'\n','') # remove newlines
            russianExamples.append(stringHolder) #each line in Russian examples will be in the form [Russian sentence - English translation]
        stressedRussianExamples = []
        for n in range(len(russianExamples)):
            russianExamples[n] = russianExamples[n].split(' - ') # each element in russianExamples is now a list with two elements: a sentence (index 0) and its translation (index 1)
            russianExamples[n][0] = markSimpleStresses(russianExamples[n][0]) #facilitates the process of finding stressed examples by stressing commonly unstressed but frequent words
            if checkSentenceForStress(russianExamples[n][0]): # checks to see which examples are stressed properly
                stressedRussianExamples.append(russianExamples[n][0])
                stressedRussianExamples.append(russianExamples[n][1])#appends the sentence and its translation separately
        return stressedRussianExamples
    except:
        logString = "no exmaples found for " + verb
        print(logString)
        with open('verblog.txt','a') as verbLog:
            print(logString, file=verbLog)
        return []

        

def getVerbList(page=0):
    """creates a list whose elements are lists with information about the verbs
    on a given page; default page is 0, corresponding to the first page
    of the dictionary"""
    page = requests.get(url)
    pageSoupObj = BeautifulSoup(page.content,'lxml') #creates Beautiful soup object from page content
    verbRows = pageSoupObj.find_all('tr') #grabs all table rows on the page and puts them in a list.
    del(verbRows[0]) #trim off the first and last three <tr> elements, as these
    del(verbRows[-3:]) #do not contain verbs
    for i in range(len(verbRows)):
        if i != 0:
            if verbRows[i].a['href'] == verbRows[i-1].a['href']:
                continue#skip verbs that point to the same conjugation
        #1 - grab the information in each row of the page on the frequency list and append it to the list for the relevant verb
        verbText = verbRows[i].text[1:-1] #gets the text of the row (getting rid of html tags and stripping leading and ending newlines)
        verbInfoList = verbText.split('\n') #returns a list of the 3 elements in each row: freq #, infinitive, meaning
        verbInfoList[0],verbInfoList[1] = verbInfoList[1],verbInfoList[0] #swap the frequency to index 1 and the infinitive to index 0
        verbInfoList[1] = padThousands(verbInfoList[1])
        #2 - go to the page of the verb listed in each row to obtain info about the aspect and conjugation, as well as examples
        verbUrl = baseUrl + verbRows[i].a['href'] #grab the link to the verb
        print('getting',verbUrl)
        verbPage = requests.get(verbUrl)
        verbSoupObj = BeautifulSoup(verbPage.content, 'lxml') #creates a beautiful soup object from the verb's conjugation page
        #3 - determine the aspect of the verb and add it to the list for the relevant verb
        verbType = verbSoupObj.find(class_='info').text #identify whether verb is perfective or imperfective
        if 'imperfective' in verbType:
            verbType = 'imperfective'
        elif 'perfective' not in verbType:
            verbType = 'imperfective'
        else:
            verbType = 'perfective'
        verbInfoList.insert(1,verbType) #insert aspect at index 1; verbInfoList now contains (infinitive, aspect, freq #, meaning)
        #4 - isolate the non-past conjugation (i.e. present for imperfective verbs or future for perfective verbs)
        #    and add the relevant forms to the list for the relevant verb
        nonPastRows = verbSoupObj.find(class_='presfut').table.find_all('tr') #creates a list of all the rows in the table containing non-past forms.
        nonPastForms = []
        for row in nonPastRows:
            rowStringList = row.text[1:-1].split('\n') # strip the newline characters from either end of each row's text content
                                            # and split the string into a three item list ([personal pronoun], [present form], [future form];
                                            #for imperfective verbs, the conjugation we are interested in will be the present forms (index 1)
                                            #For perfective verbs, we will be interested in the conjugation in the future (index 2)
            if verbType == 'imperfective':
                nonPastForms.append(rowStringList[1])
            else:
                nonPastForms.append(rowStringList[2])
        for form in nonPastForms:
            verbInfoList.append(form)
        #5 - grab imperative forms and append them to the list for the verb
        imperativeSingular = verbSoupObj.find('table').tr.text[1:-1] #find the imperative singular form in the form 'Singular\n[imperative form]'
        imperativeSingular = imperativeSingular.split('\n') #split the imperative singular form string into a list ['Singular', '[imperative form]']
        imperativeSingular = imperativeSingular[1]
        verbInfoList.append(imperativeSingular)
        imperativePlural = verbSoupObj.find('table').tr.next_sibling.next_sibling.text[1:-1]
        imperativePlural = imperativePlural.split('\n') #same as singular process
        imperativePlural = imperativePlural[1]
        verbInfoList.append(imperativePlural)
        #6 - get the past tense forms of the verb and append them to the list for the verb
        pastForms = [] #this list will contain the past forms
        for item in verbSoupObj.find(class_='past').tbody.stripped_strings:
            if countVowels(item) > 0: #test whether item is Russian string
                pastForms.append(item) #need to implement a function to append these to the textList when incorporated into getVerbList
        for form in pastForms:
            verbInfoList.append(form)
        #7 - grab at least 4 properly stressed examples and append them to the list
        examples = verbSoupObj.find('ul',class_='sentences')
        if examples is None:
            examples = False
        stressedExamples = []
        stressedExamples += getExamples(verbUrl,verbInfoList[0])
        trycount = 0
        if examples != False:
            while len(stressedExamples) < 8:
                if trycount > 4:
                    logString = 'failed to grab enough examples for ' + verbInfoList[0] + ". Gathered "+str(len(stressedExamples))+"examples."
                    print(logString)
                    with open('verblog.txt','a') as verbLog:
                        print(logString, file=verbLog)
                    break
                trycount += 1
                print('not enought examples; refreshing page')
                stressedExamples +=getExamples(verbUrl,verbInfoList[0])
        if len(stressedExamples) > 0:
            for item in stressedExamples:
#                client = boto3.client('polly', region_name='us-west-2', aws_access_key_id="somekeyhere", aws_secret_access_key="secretkey")
#                response = client.synthesize_speech(OutputFormat='mp3',Text='это мой первый текст',VoiceId='Maxim')
                verbInfoList.append(item)
        verbMasterList.append(verbInfoList)

            


getVerbList()

if not os.path.exists('./verbs'):
    os.makedirs('./verbs')

for index in range(len(verbMasterList)):
    filename = './verbs/' + verbMasterList[index][2] + transliterate(verbMasterList[index][0]) + '.txt'
    with open(filename, 'w') as verbFile:
        for num in range(len(verbMasterList[index])):
            print(verbMasterList[index][num], file=verbFile)


"""
test = requests.get('https://en.openrussian.org/ru/видеть')
testSoup = BeautifulSoup(test.content,'lxml')
russianExamples = testSoup.find_all('ul', class_='sentences') #creates a list or string whose single element/content is the exmple sentences
examplesString = stripSoupList(russianExamples,True)
sentences = [] #need to parse the string with the examples, sparating them into individual list items
stressedSentences = [] # we will test each example setence to see if every word is properly stressed
countPunctuation = 0 #will count the puctuation marks - every second mark, append sentence and translation to setences
parseStart = 0 #pointer to tell us where we are in the list
for char in range(len(examplesString)):
    if examplesString[char] == '.' or examplesString[ch`ar] == '!' or examplesString[char] == '?':
        countPunctuation += 1
        if countPunctuation % 2 == 0:
            sentences.append(examplesString[parseStart:char+1])
            parseStart = char + 1
for n in range(len(sentences)):
    sentences[n] = sentences[n].split(' - ') #sentences is now a list containing 2 element lists. The first element is a russian sentence
                                            #and the second is its translation.
for n in range(len(sentences)):
    sentences[n][0] = markSimpleStresses(sentences[n][0]) #add stresses to some basic words (this just 
                                                        #facilitates the process of finding three examples that are properly stressed)
    if checkSentenceForStress(sentences[n][0]):
        stressedSentences.append(sentences[n])


verbType = testSoup.find(class_='info').text
if 'imperfective' in verbType:
    aspect = 'imperfective'
else:
    aspect = 'perfective'
imperativeSingular = testSoup.find('table').tr.text[1:-1] #find the imperative singular form in the form 'Singular\n[imperative form]'
imperativeSingular = imperativeSingular.split('\n') #split the imperative singular form string into a list ['Singular', '[imperative form]']
imperativeSingular = imperativeSingular[1]
imperativePlural = testSoup.find('table').tr.next_sibling.next_sibling.text[1:-1]
imperativePlural = imperativePlural.split('\n') #same as singular process
imperativePlural = imperativePlural[1]
pastForms = [] #this will contain the past forms
for item in testSoup.find(class_='past').tbody.stripped_strings:
    if countVowels(item) > 0: #test whether the item in stripped_strings is Russian
        pastForms.append(item) #need to implement a function to append these to the textList when incorporated into getVerbList
#need to write: conditional based on aspect; Soup the present forms or future forms accordingly
nonPast = testSoup.find(class_='presfut').table.find_all('tr') #creates a list of all the rows in the table containing non-past forms.
nonPastForms = []
for item in nonPast:
    rowStringList = item.text[1:-1].split('\n') # strip the newline characters from either end of each row's text content
                                    # and split the string into a three item list; for imperfective verbs, the verb form will
                                    # be index 1. For perfective verbs, the verb form will be at index 2
    if aspect == 'imperfective':
        nonPastForms.append(rowStringList[1])
    else:
        nonPastForms.append(rowStringList[2])
"""
"""
#need to iterate through list above and create stripped strings generator for each element

#for i in range(0,1050, 50):
#    if i == 0:
#        targeturl = url #first page of verb listings
#    else:
#        targeturl = url + "?start=" + str(i) #subsequent pages are accessed with the addition of ?start=i, where i is a multiple of 50
#        #e.g. 'https://en.openrussian.org/list/verbs?start=50' lists verbs 51-100
#    page = requests.get(targeturl)
#    pageSoupObj = BeautifulSoup(page.content,'lxml') #creates Beautiful soup object from page content
#    verbRows = pageSoupObj.find_all('tr') #grabs all table rows on the page and puts them in a list.
#    del(verbRows[0]) #trim off rows at the start and end that do not contain verbs
#    del(verbRows[-3:])"""

