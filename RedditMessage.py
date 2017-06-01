import time
import string
import requests
from bs4 import BeautifulSoup
import sys
from random import randint
from config import *

def redditlogin(username, password,c):

    USER                = username
    PASSWD              = password
    API_TYPE            = 'json'
    OP                  = 'login-main'
    RENDERSTYLE         = 'html'
    ACTION              = 'sub'

    loginpost           = 'https://www.reddit.com/api/login/'+USER
    homeurl             = 'https://www.reddit.com'


    print "[+]Logging in as "+USER+"..."
    login_data = dict(user = USER, passwd = PASSWD, api_type = API_TYPE, op = OP)
    login = c.post(loginpost, data=login_data, headers={'User-Agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36","x-requested-with":'XMLHttpRequest','referer':'https://www.reddit.com','origin':'https://www.reddit.com'})

    if 'reddit_session' in str(login.headers):
        print '[+]Successfully logged into account '+USER
    else:
        print '[-]Could not login'


def sendmessages(userslist, messagelist,c):

    USER_LIST           = []
    MESSAGE_LIST        = []

    for line in messagelist.readlines():
                message = line.strip('\n')
                MESSAGE_LIST.append(message)

    for line in userslist.readlines():
        user = line.strip('\n')
        USER_LIST.append(user)

    for user in USER_LIST:
        MESSAGERECIEVER = user
        SELECTION = (randint(0,len(MESSAGE_LIST)-1))
        MESSAGE_TEXT = MESSAGE_LIST[SELECTION]

        print "[+]Messaging user "+user+ " with " +MESSAGE_TEXT
        #print "[+]Retrieving http://reddit.com/u/" +MESSAGERECIEVER
        r = c.get('http://reddit.com/u/'+MESSAGERECIEVER,headers={'User-Agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36","x-requested-with":'XMLHttpRequest','referer':'https://www.reddit.com','origin':'https://www.reddit.com'}).content
        soup = BeautifulSoup(r,'html.parser')
        MODHASH = soup.find('input',{ 'name': 'uh' })['value']
        REDDIT_SESSION = c.cookies['reddit_session']

        params = (
            ('app', 'res'),
                )

        data = [
            ('api_type', 'json'),
            ('from_sr', ''),
            ('subject', 'twqfqawfct'),
            ('text',MESSAGE_TEXT),
            ('to', MESSAGERECIEVER),
                ]

        sendrequest = c.post('https://www.reddit.com/api/compose', headers={'User-Agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36","x-requested-with":'XMLHttpRequest','referer':'https://www.reddit.com','origin':'https://www.reddit.com','x-modhash':MODHASH,'reddit_session':REDDIT_SESSION}, params=params, data=data)

def main():
    with requests.session() as c:

        try:
            userslist = open(usersfile,'r')
        except IOError:
            sys.exit("[-]Invalid user list!")

        try:
            messagelist = open(messagesfile,'r')
        except IOError:
            sys.exit("[-]Invalid message list!")

        redditlogin(username,password,c)
        sendmessages(userslist, messagelist,c)


if __name__ == '__main__':
    main()