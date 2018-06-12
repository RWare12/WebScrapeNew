from bs4 import BeautifulSoup
import urllib.request as req
import time
import datetime
import re

userList1 = [] #getting username from `windowbg` tag
userList2 = [] #getting username from `windowbg2` tag
message = [] #getting the post from users
quotes = [] #getting quotes from user if there is
quotesUserID = [] #user for being quoted
dateAndtime = [] #date and time of post
finalOuput = [] #will represent JSON of data scraped
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def parse(URL):

    page = req.urlopen(URL)
    soup = BeautifulSoup(page, 'html.parser') # from url

    #getting user id
    for post in soup.find_all('div',{'class':'windowbg'}):
        userList1.append(post.a.text)

    #getting user id
    for post in soup.find_all('div',{'class':'windowbg2'}):
        userList2.append(post.a.text)

    #getting post message
    for post in soup.find_all('div',{'class':'post'}):
        tempMessage = post.text.strip()
        message.append(tempMessage.replace('\xa0',''))

    #getting quotes
    for post in soup.find_all('div',{'class':'post'}):
        if post.blockquote is not None:
            tempQuote = post.blockquote.text.strip()
            quotes.append(tempQuote.replace('\xa0',''))
            if post.a is not None:
                tempQuoteUserID = post.a.text.strip().replace('Quote from: ','').split(' ')
                quotesUserID.append(tempQuoteUserID[0])
            else:
                quotesUserID.append("None")
        else:
            quotes.append("None")
            quotesUserID.append("None")

    #getting the date
    for post in soup.find_all('div',{'class':'keyinfo'}):
        dateAndtime.append(post.text.strip().replace("\n",""))

    finalDate = []

    for nDate in range(len(dateAndtime)):
        for m in range(len(months)):
            regex = months[m] + " \d{1,2}, \d{4}"
            pattern = re.compile(regex)
            matches = pattern.finditer(dateAndtime[nDate])
            for match in matches:
                toString = match.group().replace('January','01').replace('February','02').replace('March','03').replace('April','04').replace('May','05').replace('June','06').replace('July','07').replace('August','08').replace('September','09').replace('October','10').replace('November','11').replace('December','12')
                tempUnixTimeStamp = toString.replace(' ','/').replace(',','')
                toUnixTimeStamp = time.mktime(datetime.datetime.strptime(tempUnixTimeStamp, "%m/%d/%Y").timetuple())
                finalDate.append(toUnixTimeStamp)

    ctr = 0 #counter for messages to the post

    for user in range(len(userList1)):
        mainAnswer = {}
        quotesInfo = {}
        mainAnswer['user_id'] = userList1[user]
        mainAnswer['message'] = 'ignore "Quote from.." to "hh:mm:ss" message. ' + message[ctr].replace(quotes[ctr],'')
        # dictionary for quotes if the user has
        mainAnswer['quotes'] = quotesInfo
        quotesInfo['user_id'] = quotesUserID[ctr]
        quotesInfo['message'] = quotes[ctr]
        # timestamp UNIX
        mainAnswer['date_posted'] = finalDate[ctr]
        ctr += 1
        finalOuput.append(mainAnswer)
        if user < len(userList1)-1:
            mainAnswer = {}
            quotesInfo = {}
            mainAnswer['user_id'] = userList2[user]
            mainAnswer['message'] = 'ignore "Quote from.." to "hh:mm:ss" message. ' + message[ctr].replace(quotes[ctr],'')
            # dictionary for quotes if the user has
            mainAnswer['quotes'] = quotesInfo
            quotesInfo['user_id'] = quotesUserID[ctr]
            quotesInfo['message'] = quotes[ctr]
            # timestamp UNIX
            mainAnswer['date_posted'] = finalDate[ctr]
            ctr += 1
            finalOuput.append(mainAnswer)

    return finalOuput

