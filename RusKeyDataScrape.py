import requests
import unicodedata
from bs4 import BeautifulSoup
import sys
baseUrl = 'https://en.openrussian.org'
url = 'https://en.openrussian.org/list/verbs'
verbMasterList = [] #this will be a master list containing
              #a list for each verb as its elements
verbFormsKey = ['infinitive','aspect','frequency','meaning','1st singular',
                '2nd singular', '3rd singular', '1st plural','2nd plural',
                '3rd plural', 'imperative singular','imperative plural',
                ] #this contains the name of each element appended for an individual verb
commonEndUnstressed = ["его","она","они","себе","тебе","меня","тебя","себя","уже","чего","ничего"] #list of words commonly left unstressed in examples that have stressed final vowels


def countVowels(word):
    """takes a string and returns the number of Russian vowels"""
    #For use in checking whether a word has a stress
    count = 0
    for letter in word:
        if letter in "аеёиоуыэюя":
            count += 1
    return count

def checkWordForStress(word):
    """takes a string and returns True if the word is one syllable long or has
    two or more syllables, one of which is accented; returns False otherwise"""
    #limitation here would be stressed prepositions...
    if countVowels(word) > 1 and chr(769) not in word and 'ё' not in word:
        return False
    else:
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
        result = " ".join(sentence)
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
        #7 - grab at least 3 properly stressed examples and append them to the list
        russianExamples = verbSoupObj.find_all('ul', class_='sentences')
        examplesString = stripSoupList(russianExamples,True) #returns a string of all the text contents of ul items of class sentences
        sentences = [] #the examples will be parsed from the examples string into this list
        stressedSentences = [] #from the sentences list, the propperly stressed examples will be filtered into this list
        countPunctuation = 0 #the senteces list will be parsed by punctuation - every second punctuation mark, we have gotten
                            #to the end of a Russian sentence/translation pair.
        parseStart = 0 #this pointer will adjust as we iterate through the string to point at the beginning of the next example
        for num in range(len(examplesString)):
            if examplesString[num] == '.' or examplesString[num] == '!' or examplesString[num] == '?':
                countPunctuation += 1
                if countPunctuation % 2 == 0: # if the number of punctuation marks is even, we have a full example/translation pair
                    sentences.append(examplesString[parseStart:num+1]) #add the example/translation pair
                    parseStart = num + 1 #adjust our starting pointer so that it points to the beginning of the next example
        for n in range(len(sentences)):
            sentences[n] = sentences[n].split(' - ') #sentences now contains lists as its elements; each list element contains a russian sentence (index 0)
                                                    #and its translation (index 1).
            sentences[n][0] = markSimpleStresses(sentences[n][0]) #add stresses to some basic words (this just 
                                                                #facilitates the process of finding three examples
                                                                #that are properly stressed)
            if checkSentenceForStress(sentences[n][0]):
                stressedSentences.append(sentences[n])
        trycount = 0
        while len(stressedSentences) < 3:
            if trycount > 4:
                print('failed to grab examples for',verbInfoList[0])
                break
            trycount += 1
            print('less than three examples; reloading')
            verbPage = requests.get(verbUrl)
            verbSoupObj = BeautifulSoup(verbPage.content, 'lxml') #creates a beautiful soup object from the verb's conjugation page
            russianExamples = verbSoupObj.find_all('ul', class_='sentences')
            examplesString = stripSoupList(russianExamples,True) #returns a string of all the text contents of ul items of class sentences
            sentences = [] #the examples will be parsed from the examples string into this list
            stressedSentences = [] #from the sentences list, the propperly stressed examples will be filtered into this list
            countPunctuation = 0 #the senteces list will be parsed by punctuation - every second punctuation mark, we have gotten
                                #to the end of a Russian sentence/translation pair.
            parseStart = 0 #this pointer will adjust as we iterate through the string to point at the beginning of the next example
            for num in range(len(examplesString)):
                if examplesString[num] == '.' or examplesString[num] == '!' or examplesString[num] == '?':
                    countPunctuation += 1
                    if countPunctuation % 2 == 0: # if the number of punctuation marks is even, we have a full example/translation pair
                        sentences.append(examplesString[parseStart:num+1]) #add the example/translation pair
                        parseStart = num + 1 #adjust our starting pointer so that it points to the beginning of the next example
            for n in range(len(sentences)):
                sentences[n] = sentences[n].split(' - ') #sentences now contains lists as its elements; each list element contains a russian sentence (index 0)
                                                        #and its translation (index 1).
                sentences[n][0] = markSimpleStresses(sentences[n][0]) #add stresses to some basic words (this just 
                                                                    #facilitates the process of finding three examples
                                                                    #that are properly stressed)
                if checkSentenceForStress(sentences[n][0]):
                    stressedSentences.append(sentences[n])
        if len(stressedSentences) > 0:
            for item in stressedSentences:
                verbInfoList.append(item)
        verbMasterList.append(verbInfoList)
        

getVerbList()


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
    if examplesString[char] == '.' or examplesString[char] == '!' or examplesString[char] == '?':
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
