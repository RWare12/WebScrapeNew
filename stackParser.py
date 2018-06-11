from bs4 import BeautifulSoup
import urllib.request as req

userList1 = [] #getting username from `windowbg` tag
userList2 = [] #getting username from `windowbg2` tag
message = [] #getting the post from users
quotes = [] #getting quotes from user if there is

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
    else:
        quotes.append("None")

print("userList1: ",userList1) 
print("userList2: ",userList2) 
print("message: ",message) 
print("quotes: ", quotes)
