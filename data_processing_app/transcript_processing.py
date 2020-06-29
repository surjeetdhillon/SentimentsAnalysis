import csv
import pandas as pd
from monkeylearn import MonkeyLearn
from collections import defaultdict
from numpy import empty
import json
from profanity_filter import ProfanityFilter
from textblob import TextBlob



def main():
    convertfiletocsv()
    #findSentiments()
    #sentimentsAnalysis()
    meetingNotes()

def meetingNotes():
    ##Filter Profanity Filter 
    #applyProfanityFilter()
    
    columns = defaultdict(list) 

    try:
        with open('media/recording1/transcript.csv') as f:
            reader = csv.DictReader(f) 
            for row in reader: 
                for (k,v) in row.items(): 
                    columns[k].append(v)
        sentences = columns['sentence']
        
        ##Perform grammer check on all script
        grammerCheck()

        ##Find agenda of meeting and notes
        agenda = findAgenda(sentences)
        meetingNotes = createMeetingNotes(sentences)
        nextSteps = createNextSteps(sentences)

        print(agenda)
        print(meetingNotes)
        print(nextSteps)

    finally:
        f.close()




def createMeetingNotes(sentence):
    meetingNotes = 'Meeting Notes : \n'
    count = 1
    for s in sentence:
        if len(s) < 5:
            continue
        elif 'Thanks for attending' in s:
            continue
        elif 'next step' in s:
            continue
        else:
            meetingNotes = meetingNotes + str(count) + ': ' + s + '\n'
            count += 1
    return meetingNotes



def createNextSteps(sentence):
    nextSteps = 'Next Steps :\n'
    count = 1
    for s in sentence:
        if len(s) < 5:
            continue
        elif 'agenda' in s:
            continue
        elif 'next step' in s:
            nextSteps = nextSteps + str(count) + ': ' + s + '\n'
            count += 1

    return nextSteps



def applyProfanityFilter():
    pf = ProfanityFilter()
    pf.censor_char = '@'

    with open('media/recording1/transcript.csv', mode='w+') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_reader = csv.DictReader(csv_file)            
        for row in csv_reader:
            if pf.is_clean(row['sentence']):
                continue
            else:
                csv_writer.writerow(['***', '****', '****' , '*****', '*****'])
        csv_file.close



def findAgenda(sentence):
    agenda = 'Nobody spoke about Agenda!'
    for s in sentence:
        if 'agenda' in s:
            ## This method can be trained from a model to find an agenda
            ind1 = len(s)-s.index('agenda')
            agenda = 'Agenda of meeting: \n'+ s[-ind1+1:]
            if 'to' in agenda:
                ind2 = ind1-agenda.index('to')
                agenda = 'Agenda of meeting: \n' + s[-ind2+1:]
            break
    return agenda

def sentimentsAnalysis():   
    columns = defaultdict(list) 
    with open('media/recording1/transcript.csv') as f:
         reader = csv.DictReader(f) 
         for row in reader: 
             for (k,v) in row.items(): 
                 columns[k].append(v)

    positiveCounter = 0
    negativeCounter = 0
    neutralCounter = 0
    ml = MonkeyLearn('ab7ba9286a2c0793d287a35eef87b272db9eac8c')
    model_id = 'cl_pi3C7JiL'
    
    for s in columns['sentence']:
        li = [s]
        result = ml.classifiers.classify(model_id, li).body
        print(result[0]['classifications'][0]['tag_name'])
        if result[0]['classifications'][0]['tag_name'] == 'Positive':
            positiveCounter += 1
        elif result[0]['classifications'][0]['tag_name'] == 'Neutral':
            neutralCounter += 1
        elif result[0]['classifications'][0]['tag_name'] == 'Negative':
            negativeCounter += 1  

    print('Positive '+positiveCounter)
    print('Negative '+negativeCounter)
    print('Neutral '+neutralCounter) 

    f.close()
    return "Sentiments result => Neutral-"+neutralCounter+" Negative-"+negativeCounter+" Positive-"+ positiveCounter
    



###Make Sentimental decision###
def findSentiments():
    filepath_dict = {'yelp':   'sentimentlabelledsentences/yelp_labelled.txt',
                 'amazon': 'sentimentlabelledsentences/amazon_cells_labelled.txt',
                 'imdb':   'sentimentlabelledsentences/imdb_labelled.txt'}

    df_list = []
    for source, filepath in filepath_dict.items():
        df = pd.read_csv(filepath, names=['sentence', 'label'], sep='\t')
        df['source'] = source  # Add another column filled with the source name
        df_list.append(df)

    df = pd.concat(df_list)
    print(df.iloc[0])


###Converting Transcript to CSV File###    
def convertfiletocsv():
    try:
        csv_file = open("media/recording1/transcript.csv", "a")
        csv_file.write('sr,'+'starttime,'+'stoptime,'+'speaker,'+'sentence')
        with open('media/recording1/GMT20200627-193326_Surjeet-Dh.transcript.vtt', 'r') as in_file:
            stripped = (line.strip() for line in in_file)
            for line in stripped:
                line = line.replace(', ',' ')
                #print(line)
                if line == 'WEBVTT':
                    continue
                elif line.isnumeric():
                    csv_file.write(line+',')
                elif ' --> ' in line:
                    time = line.split(" --> ")
                    for ti in time:
                        csv_file.write(ti+',')
                elif ':' in line:
                    tex = line.split(":")
                    for t in tex:
                        csv_file.write(t+',')
                else:
                    csv_file.write('\n')
    finally:
        in_file.close()
        csv_file.close()


#Grammer Check function
def grammerCheck():
    with open('media/recording1/transcript.csv', mode='w+') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_reader = csv.DictReader(csv_file)
            
        for row in csv_reader:
            text = TextBlob(row['sentence'])
            #csv_writer.writerow([row['sr'], row['starttime'], row['stoptime'] , row['speaker'], text])                    
    csv_file.close

# Function to convert   
def listToString(s):  
    str1 = " "     
    return (str1.join(s))

if __name__ == '__main__':
    main()