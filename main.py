import stackParser
import saveJsonFile
import re

URL = ''

while(URL is not 'q'):
    print('Enter \'q\' to exit!')
    URL = input('ENTER URL: ') #getting URL

    inputURL = re.findall('https?://forums.abs-cbn.com+/(?:[-\w.!()]|(?:%[.]))+/(?:[-\w.!()]|(?:%[.]))+', URL)

    if len(inputURL) is not 0:
            result = stackParser.parse(URL)
            saveJsonFile.saveFile(result)

    elif URL is 'q':
        exit()

    else:
            print("Invalid URL!")

