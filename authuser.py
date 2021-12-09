import requests

# from PyQt6 import QtWebEngineWidgets
# from PyQt6.QtCore import QUrl
# import re
# from PyQt6.QtWebEngineCore import *
# from PyQt6.QtWebEngineQuick import *
# from PyQt6.QtWebEngineWidgets import *
# from PyQt6.QtWebSockets import *
# from PyQt6.QtWidgets import *
# import urllib
# import urllib3



class authenticate :

    def __init__(self, email, password, accounttype):
        self.email = email
        self.password = password
        self.account = accounttype
        self.__auth__()
        
    def __auth__(self):
        if self.account == 'mojang':
            return self.__authmojang__()
        elif self.account == 'microsoft':
            raise Exception('Microsoft Authentication is still in development')
            # in the future this will call self.__authmicrosoft__()
        else:
            raise ValueError('authentication expected \'mojang\' or \'microsoft\' account type, but received otherwise')

    def __authmojang__(self):
        postdata = '{"agent" : "Minecraft", "username" : "%s", "password": "%s", "requestUser" : "false"}'%(self.email, self.password)
        authrequest = requests.post(url='https://authserver.mojang.com/authenticate',data=postdata,headers={"Content-Type" : "application/json"})
        
        returneddata = eval(authrequest.content)
        if authrequest.status_code == 200:
            self.authtoken, self.username, self.uuid = returneddata['accessToken'], returneddata['selectedProfile']['name'], returneddata['selectedProfile']['id']
            self.status = 'OK'
        else:
            self.error = returneddata["errorMessage"]
            self.status = 'Failed'
        
        
if __name__ == "__main__":
    authdata = authenticate(input('Username: '), input('Password: '), input('Account Type: '))
    print(authdata.authtoken)



# def microsoftauth():
#     email = 'emailTest'
#     password = 'passwordTest'
#     sFFTagAndUrlPost = getSFFTagAndUrlpost()
#     postrequest = postMicrosoft(sFFTagAndUrlPost,email,password)
#     #return postrequest
#     #returncode = checkMicrosoftRecieved()
# 
# 
# def getSFFTagAndUrlpost():
#     urlresponse = requests.get("https://login.live.com/oauth20_authorize.srf?client_id=000000004C12AE6F&redirect_uri=https://login.live.com/oauth20_desktop.srf&scope=service::user.auth.xboxlive.com::MBI_SSL&display=touch&response_type=token&locale=en",)
#     sFFTag = re.search('(?<=value=")(.+?)(?=\")', urlresponse.text)
#     urlPost = re.search('(?<=urlPost:\')(.+?)(?=[\'])', urlresponse.text)
#     return [sFFTag, urlPost]
# 
# def encode(sFFTagAndUrlPost,email,password):
# 
#     sFFTag = sFFTagAndUrlPost[0].group(1)
#     urlPost = sFFTagAndUrlPost[1].group(1)
#     encodedSFFTag = urllib.parse.quote(sFFTag)
#     encodedEmail = urllib.parse.quote(email)
#     encodedPassword = urllib.parse.quote(password)
#     
#     Postdata = "login={}&loginfmt={}&passwd={}&PPFT={}".format(encodedEmail,encodedEmail,encodedPassword,encodedSFFTag)
#     
# 
#     Request1 = QWebEngineHttpRequest(QUrl = urlPost, method=QWebEngineHttpRequest.Post)
#     #postRequest(QUrl) > QWebEngineHttpRequest
#     print (Request1.postData())
# 
# 
#     
#     #postrequest = requests.post(url=urlPost, data=postdata, headers={"Content-Type":"application/x-www-form-urlencoded"})
#     #rdr1 = re.search('(?<=URL=)(.+?)(?=\")', postrequest.text)
#     #print(rdr1.group(1))
#     #print(postrequest.status_code)
#     #print(postrequest.is_permanent_redirect)
#     #print(postrequest.is_redirect)
#     #return postrequest
# def checkMicrosoftRecieved(postrequest):
#     pass
# 
# if __name__ ==  "__main__":
#     microsoftauth()
#     #print('\t#######AAAA-URL####\n')
#     #print(postrequest.url)
#     #print('\t#######AAAA-TEXT####\n')
#     #print(postrequest.text)
#     #print('\t#######AAAA-END####\n')