import os
import requests
import boto3
fileList = os.listdir('./verbs')
fileList.sort()
for file in fileList:
    with open('./verbs/'+ file, 'r') as verbFile:
        verbFileLinesList = verbFile.readlines()
        verbFormsString = "<speak>"+verbFileLinesList[0] + '<break time="0.5s"/>'
        for i in range(4,16):
            verbFormsString += verbFileLinesList[i]
            if i != 15:
                verbFormsString += '<break time="0.5s"/>'
        verbFormsString += '</speak>'
        verbFormsString = verbFormsString.replace(u'\n','')
        verbExamplesList = []
        for i in range(16,len(verbFileLinesList),2):
            verbExamplesList.append(verbFileLinesList[i].replace(u'\n',''))
        print(verbFormsString)
        for i in verbExamplesList:
            print(i)