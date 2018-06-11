from bs4 import BeautifulSoup
import urllib.request as req

userList1 = [] #getting username from `windowbg` tag
userList2 = [] #getting username from `windowbg2` tag
message = [] #getting the post from users
quotes = [] #getting quotes from user if there is
quotesUserID = [] #user for being quoted
dataAndtime = [] #date and time of post
finalOuput = [] #will represent JSON of data scraped

page = req.urlopen('http://forums.abs-cbn.com/bagani-(march-5-2018-present)/alamat/')
soup = BeautifulSoup(page, 'html.parser') # from url


for post in soup.find_all('div',{'class':'windowbg'}):
    userList1.append(post.a.text)

for post in soup.find_all('div',{'class':'windowbg2'}):
    userList2.append(post.a.text)

for post in soup.find_all('div',{'class':'post'}):
    message.append(post.text.strip())

for post in soup.find_all('div',{'class':'post'}):
    if post.blockquote is not None:
        quotes.append(post.blockquote.text.strip())
        quotesUserID.append(post.a.text)
    else:
        quotes.append("None")
        quotesUserID.append("None")

for post in soup.find_all('div',{'class':'smalltext'}):
    dataAndtime.append(post.text.strip())



print(len(message))

ctr = 0 #counter for messages to the post

for user in range(len(userList1)):
    mainAnswer = {}
    quotesInfo = {}
    mainAnswer['user_id'] = userList1[user]
    # mainAnswer['message'] = message[ctr]
    mainAnswer['quotes'] = quotesInfo
    quotesInfo['user_id'] = quotesUserID[ctr]
    ctr += 1
    finalOuput.append(mainAnswer)
    if user < len(userList1)-1:
        mainAnswer = {}
        mainAnswer['user_id'] = userList2[user]
        # mainAnswer['message'] = message[ctr]
        mainAnswer['quotes'] = quotesInfo
        quotesInfo['user_id'] = quotesUserID[ctr]
        ctr += 1
        finalOuput.append(mainAnswer)



# print("quotes: ",quotes)
# print("quotesUserID: ",quotesUserID)
# print("dateAndtime: ",dataAndtime)

print(finalOuput) #final
