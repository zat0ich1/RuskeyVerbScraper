import os
import boto3
from awskeys import *

from contextlib import closing
# awskeys is a python file containing two variable assignments:
#keyid is assigned to the access key id passed to the  aws_access_key_id
#param in the synthesize_speech call; secretkey is the aws secret key
#passed to the aws_secret_access_key parameter;
prompt = "Male or female voice for this exapmle? Type f or enter for female, m for male: "
fileList = os.listdir('./verbs')
fileList.sort()

client = boto3.client('polly', region_name='us-west-2', aws_access_key_id=keyid, aws_secret_access_key=secretkey)

def containsI(sentence):
    """returns True if a sentence contains the Russian pronoun я; false otherwise"""
    sentenceList = sentence.split(' ')
    if 'я' in sentenceList or 'Я' in sentenceList:
        return True
    else:
        return False

def getAudio(fileNameStr, translateString, voiceName='Tatyana', mode='text'):
    """makes an amazon polly api call to save an mp3 file of tts for text in voiceID's voice;
        fileNameStr - a string for the filename (e.g. 'file1.mp3');
        translateString - a string of the text you want turned into audio (with or without ssml tags - see next param);
        mode - 'ssml' or 'text' (default);
        voice - a string of the voice name you wish to use; for Russian either 'Tatyana' or 'Maxim'"""
    response = client.synthesize_speech(OutputFormat='mp3',Text=translateString, TextType=mode, VoiceId=voiceName)
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as voiceStream:
            try:
                with open(fileNameStr, 'bw') as audioFile:
                    audioFile.write(voiceStream.read())
                    print('writing to file',fileNameStr)
            except:
                print("An error occurred when requesting audio for",translateString)
for file in fileList:
    audioFileName = './verbs/' + file[:-4] + '.mp3' #grabs text file name and replace .txt with .mp3
    with open('./verbs/'+ file, 'r') as verbFile: #open each file in the ./verbs directory
        verbFileLinesList = verbFile.readlines() #create a list containing each line of the file as an element
        verbFormsString = "<speak>"+verbFileLinesList[0] + '<break time="0.5s"/>'#add a ssml .5 second break after the infinitive
        for i in range(4,16):
            verbFormsString += verbFileLinesList[i]
            if i != 15:
                verbFormsString += '<break time="0.5s"/>' #add a .5 second ssml break after the remaining conjugated forms (except the last one)
        verbFormsString += '</speak>'
        verbFormsString = verbFormsString.replace(u'\n','') #remove the newline characters throughout
        verbExamplesList = []
        for i in range(16,len(verbFileLinesList)):
            verbExamplesList.append(verbFileLinesList[i].replace(u'\n','')) #adds each example and translation to the list without newlines
        print("sending " + verbFormsString + " to AWS Polly")
        getAudio(fileNameStr=audioFileName, translateString=verbFormsString, voiceName='Tatyana', mode='ssml')
        print('getting',verbFormsString,'as',audioFileName)
        for i in range(0,len(verbExamplesList)-1,2):
            print ('=' * 40)
            print (verbExamplesList[i])
            print (verbExamplesList[i+1])
            exampleAudioFileName = audioFileName[:-4] + str(i//2) + audioFileName[-4:] #add example number to file name
            if containsI(verbExamplesList[i]):
                voice = input (prompt)
                while voice != 'm' and voice != 'f' and voice != '':
                    print ('invalid selection')
                    voice = input (prompt)
                if voice == 'm':
                    print('getting',verbExamplesList[i],'as',exampleAudioFileName)
                    getAudio(fileNameStr=exampleAudioFileName, translateString=verbExamplesList[i], voiceName='Maxim')
                elif voice == 'f' or voice == '':
                    print('getting',verbExamplesList[i],'as',exampleAudioFileName)
                    getAudio(fileNameStr=exampleAudioFileName, translateString=verbExamplesList[i])
            else:
                print('getting',verbExamplesList[i],'as',exampleAudioFileName)
                getAudio(fileNameStr=exampleAudioFileName, translateString=verbExamplesList[i])