import json
from requests import RequestException, head
import requests
from urllib.parse import urlencode, quote
import re

# from MBasiC.webbrowser import requestPage
import webrequest


class authenticate:
    def __init__(self, email, password, accounttype):
        self.email = email
        self.password = password
        self.account = accounttype
        self.__auth__()

    def __auth__(self):
        if self.account == "mojang":
            return self.__authmojang__()
        elif self.account == "microsoft":
            self.__authmicrosoft__()
        else:
            raise ValueError(
                "Authentication expected 'mojang' or 'microsoft' account type, but received otherwise:"
                + self.account
            )

    def __authmojang__(self):
        postdata = (
            '{"agent" : "Minecraft", "username" : "%s", "password": "%s", "requestUser" : "false"}'
            % (self.email, self.password)
        )
        authrequest = requests.post(
            url="https://authserver.mojang.com/authenticate",
            data=postdata,
            headers={"Content-Type": "application/json"},
        )

        returneddata = eval(authrequest.content)
        if authrequest.status_code == 200:
            self.authtoken, self.username, self.uuid = (
                returneddata["accessToken"],
                returneddata["selectedProfile"]["name"],
                returneddata["selectedProfile"]["id"],
            )

            self.status = "OK"
        else:
            self.error = returneddata["errorMessage"]
            self.status = "Failed"

    def __authmicrosoft__(self):
        # Setup
        webapp = webrequest.app()

        ### SIGNING INTO MICROSOFT

        prepUrl = "https://login.live.com/oauth20_authorize.srf?client_id=000000004C12AE6F&redirect_uri=https://login.live.com/oauth20_desktop.srf&scope=service::user.auth.xboxlive.com::MBI_SSL&display=touch&response_type=token&locale=en"
        prepGot = webapp.requestPage(url=prepUrl, method="get")
        sFTTag = re.search('value="(.+?)"', prepGot.html).group(1)
        urlPost = re.search("urlPost:'(.+?)'", prepGot.html).group(1)
        print("sFFTag\n\n" + sFTTag + "\n")
        print("urlPost\n\n" + urlPost)

        email = "emailTest"
        password = "passwordTest"
        postDict = {
            "login": email,
            "loginfmt": email,
            "passwd": password,
            "PPFT": sFTTag,
        }

        postInfo = urlencode(postDict, quote_via=quote)

        postHeaders = {"Content-Type": "application/x-www-form-urlencoded"}
        postGot = webapp.requestPage(
            url=urlPost, method="post", headers=postHeaders, data=postInfo
        )

        finalUrl = postGot.url

        if finalUrl == urlPost:
            raise ValueError("Login failed for reasons that we don't care about")

        microsoftResponse = {
            v.split("=")[0]: v.split("=")[1]
            for v in finalUrl.toString().split("#")[1].split("&")
        }
        print(microsoftResponse)
        print("\n")

        ##### Warning, you are about to leave the last working part of this script.

        ### SIGNING INTO XBOX LIVE

        xboxPostBody = urlencode(
            {
                "Properties": {
                    "AuthMethod": "RPS",
                    "SiteName": "user.auth.xboxlive.com",
                    "RpsTicket": f'{microsoftResponse["access_token"]}',
                },
                "RelyingParty": "http://auth.xboxlive.com",
                "TokenType": "JWT",
            },
            quote_via=quote,
        )

        bodyTest = {
            "Properties": {
                "AuthMethod": "RPS",
                "SiteName": "user.auth.xboxlive.com",
                "RpsTicket": f'"{microsoftResponse["access_token"]}"',
            },
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT",
        }

        jsonHeaders = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        req1 = requests.post(
            url="https://user.auth.xboxlive.com/user/authenticate",
            json=bodyTest,
        )

        print("Requests method:")
        print(req1.text)
        print(req1.status_code)
        print(req1.reason)

        print("Webapp method:")

        xboxRequest = webapp.requestPage(
            url="https://user.auth.xboxlive.com/user/authenticate",
            method="post",
            data=bodyTest,
            headers=jsonHeaders,
        )

        xboxDict = json.loads(re.search("({.+})", xboxRequest.html).group(1))
        xboxToken, xboxUhs = (
            xboxDict["Token"],
            xboxDict["DisplayClaims"]["xui"][0]["uhs"],
        )

        XSTSData = {
            "Properties": {"SandboxId": "RETAIL", "UserTokens": [f"{xboxToken}"]},
            "RelyingParty": "rp://api.minecraftservices.com/",
            "TokenType": "JWT",
        }

        XSTSRequest = webapp.requestPage(
            url="https://xsts.auth.xboxlive.com/xsts/authorize",
            method="post",
            data=XSTSData,
            headers=jsonHeaders,
        )

        XSTSDict = json.loads(re.search("({.+})", XSTSRequest.html).group(1))
        XSTSToken = XSTSDict["Token"]

        

        # https://api.minecraftservices.com/authentication/login_with_xbox


if __name__ == "__main__":
    # authdata = authenticate(
    # input("Username: "), input("Password: "), input("Account Type: ")
    # )
    authenticate(email=None, password=None, accounttype="microsoft")
    # print(authdata.authtoken)
