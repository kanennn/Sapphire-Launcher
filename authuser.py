import requests
import re
import PyQt6

def microsoftauth():
    email = 'emailTest'
    password = 'passwordTest'
    sFFTagAndUrlPost = getSFFTagAndUrlpost()
    postrequest = postMicrosoft(sFFTagAndUrlPost,email,password)
    #return postrequest
    #returncode = checkMicrosoftRecieved()


def getSFFTagAndUrlpost():
    urlresponse = requests.get("https://login.live.com/oauth20_authorize.srf?client_id=000000004C12AE6F&redirect_uri=https://login.live.com/oauth20_desktop.srf&scope=service::user.auth.xboxlive.com::MBI_SSL&display=touch&response_type=token&locale=en",)
    sFFTag = re.search('(?<=value=")(.+?)(?=\")', urlresponse.text)
    urlPost = re.search('(?<=urlPost:\')(.+?)(?=[\'])', urlresponse.text)
    return [sFFTag, urlPost]

def postMicrosoft(sFFTagAndUrlPost,email,password):
    sFFTag = sFFTagAndUrlPost[0].group(1)
    urlPost = sFFTagAndUrlPost[1].group(1)
    encodedSFFTag = urllib.parse.quote(sFFTag)
    encodedEmail = urllib.parse.quote(email)
    encodedPassword = urllib.parse.quote(password)
    #print(encodedSFFTag)
    postdata = "login={}&loginfmt={}&passwd={}&PPFT={}".format(encodedEmail,encodedEmail,encodedPassword,encodedSFFTag)
    #print(postdata)
    postrequest = requests.post(url=urlPost, data=postdata, headers={"Content-Type":"application/x-www-form-urlencoded"})
    rdr1 = re.search('(?<=URL=)(.+?)(?=\")', postrequest.text)
    print(rdr1.group(1))
    print(postrequest.status_code)
    print(postrequest.is_permanent_redirect)
    print(postrequest.is_redirect)
    return postrequest
def checkMicrosoftRecieved(postrequest):
    pass

if __name__ ==  "__main__":
    microsoftauth()
    #print('\t#######AAAA-URL####\n')
    #print(postrequest.url)
    #print('\t#######AAAA-TEXT####\n')
    #print(postrequest.text)
    #print('\t#######AAAA-END####\n')