import os
import requests
import boto3
import awskeys
from contextlib import closing
# awskeys is a python file containing two variable assignments:
#keyid is assigned to the access key id passed to the  aws_access_key_id
#param in the synthesize_speech call; secretkey is the aws secret key
#passed to the aws_secret_access_key parameter;
promptOne = "Send example above to AWS? Type enter or y to continue or n to cancel: "
promptTwo = "Male or female voice for this exapmle? Type m or enter for male, f for female, or c to cancel "
count = 0
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
        for i in range(16,len(verbFileLinesList)):
            verbExamplesList.append(verbFileLinesList[i].replace(u'\n',''))
        print("sending " + verbFormsString + " to AWS Polly")
        #add code to create mp3 from verbFormsString
        for i in range(0,len(verbExamplesList)-1,2):
            print ('=' * 40)
            print (verbExamplesList[i])
            print (verbExamplesList[i+1])
            sendToAWS = 'n'
            count += 1
#            sendToAWS = input(promptOne)
#            while sendToAWS != 'y' and sendToAWS != 'n' and sendToAWS != '':
#                print ("invalid selection")
#                sendToAWS = input(promptOne)
            if sendToAWS == 'n':
                continue
            elif sendToAWS == 'y' or sendToAWS == '':
                voice = input (promptTwo)
                while voice != 'm' and voice != 'f' and voice != 'c' and voice != '':
                    print ('invalid selection')
                    voice = input (promptTwo)
                if voice == 'm' or voice == '':
                    print("aws call with male voice")
                elif voice == 'f':
                    print("aws call with female voice")
                elif voice == 'c':
                    continue
print(count)