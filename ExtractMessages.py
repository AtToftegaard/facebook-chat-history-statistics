from os import write
import sys
from bs4 import BeautifulSoup
import bs4
import funcs as func
import pandas as pd
import csv

filenames = sys.argv[1:]
texts = []
dates = []
senders = []
isImage = []
reactions = []
count = 0

for file in filenames:
    with open(file, encoding="utf8") as fp:
        soup = BeautifulSoup(fp, 'lxml')
    messageEntry = soup.find_all('div', class_='pam _3-95 _2pi0 _2lej uiBoxWhite noborder')
    for entry in messageEntry:
        textarea = entry.find('div', class_='_3-96 _2let') #Find overall message-tag
        if(textarea):
            text = textarea.find_all('div')[2].text #Find the 'content'
            if(text): #If a text message
                texts.append(text)
                isImage.append(False)
            else: #If an image
                texts.append(None)
                isImage.append(True)
            dates.append(entry.find('div', class_='_3-94 _2lem').text) #save date
            senders.append(entry.find('div', class_='_3-96 _2pio _2lek _2lel').text) #save sender
            reacs = textarea.find('ul', class_="_tqp") #find reactions
            if reacs:
                reactionsList = reacs.find_all('li')
                finalreactions = []
                for reaction in reactionsList:
                    finalreactions.append(reaction.text)
                reactions.append(finalreactions)
            else:
                reactions.append([]) #columns need equal length
            count = count + 1


HandledReactions = []
idx = 0
for reactionList in reactions:
    if len(reactionList) > 0:
        for reaction in reactionList:
            emojiAndName = str.split(reaction)
            HandledReactions.append([emojiAndName[0], ' '.join(emojiAndName[1:],), texts[idx], senders[idx], dates[idx]])
    idx = idx + 1

print("length of reactions: ", len(reactions))
print("length of texts: ", len(texts))
print("length of reactions", len(HandledReactions))

reactionsDf = pd.DataFrame(HandledReactions, columns=['Emoji', 'Receiver', 'Message', 'Sender', 'Date'])
reactionsDf.to_csv('reactions.csv')
dict = {'Message': texts, 'Date': dates, 'Sender': senders, 'isImage': isImage}
df = pd.DataFrame(dict)
df.to_csv('messages.csv')
print("Done. ", count)

