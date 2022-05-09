import json
import requests
from urllib.parse import urlencode, quote
import re

import MBasiC.webrequest as webrequest


class authenticate:
    def __init__(self, email, password, accounttype):
        self.email = email
        self.password = password
        self.account = accounttype
        print("* Authenticating...")
        self.__auth__()

    def __auth__(self):
        if self.account == "mojang":
            return self.__authmojang__()
        elif self.account == "microsoft":
            return self.__authmicrosoft__()
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

            self.status = 0
        else:
            self.error = returneddata["errorMessage"]
            self.status = 1

    def __authmicrosoft__(self):
        # Setup
        webapp = webrequest.app()
        email = self.email
        password = self.password

        ### SIGNING INTO MICROSOFT

        # Prep

        prepRequest = webapp.requestPage(
            url="https://login.live.com/oauth20_authorize.srf?client_id=000000004C12AE6F&redirect_uri=https://login.live.com/oauth20_desktop.srf&scope=service::user.auth.xboxlive.com::MBI_SSL&display=touch&response_type=token&locale=en",
            method="get",
        )
        prepSFTTag = re.search('value="(.+?)"', prepRequest.html).group(1)
        prepUrlPost = re.search("urlPost:'(.+?)'", prepRequest.html).group(1)

        # Actual

        msPostDict = {
            "login": email,
            "loginfmt": email,
            "passwd": password,
            "PPFT": prepSFTTag,
        }

        msData = urlencode(msPostDict, quote_via=quote)

        msRequest = webapp.requestPage(
            url=prepUrlPost,
            method="post",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=msData,
        )

        finalUrl = msRequest.url

        if finalUrl == prepUrlPost:
            self.status = 1
            self.error = "Login failed for unknown reasons (reasons I didn't code for)"
            return

        if "Sign in to" in msRequest.html:
            self.status = 1
            self.error = "Invalid Credentials"
            return

        if "Help us protect your account" in msRequest.html:
            self.status = 1
            self.error = "Two factor authentication is enabled for this account which is not currently supported"
            return

        microsoftResponse = {
            v.split("=")[0]: v.split("=")[1]
            for v in finalUrl.toString().split("#")[1].split("&")
        }

        ### SIGNING INTO XBOX LIVE

        xboxData = {
            "Properties": {
                "AuthMethod": "RPS",
                "SiteName": "user.auth.xboxlive.com",
                "RpsTicket": f'"{microsoftResponse["access_token"]}"',
            },
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT",
        }

        xboxRequest = requests.post(
            url="https://user.auth.xboxlive.com/user/authenticate",
            json=xboxData,
        )

        xboxDict = json.loads(xboxRequest.text)
        xboxToken, xboxUhs = (
            xboxDict["Token"],
            xboxDict["DisplayClaims"]["xui"][0]["uhs"],
        )

        ### GETTING XSTS TOKEN

        XSTSData = {
            "Properties": {"SandboxId": "RETAIL", "UserTokens": [f"{xboxToken}"]},
            "RelyingParty": "rp://api.minecraftservices.com/",
            "TokenType": "JWT",
        }

        XSTSRequest = requests.post(
            url="https://xsts.auth.xboxlive.com/xsts/authorize",
            json=XSTSData,
        )

        XSTSDict = json.loads(XSTSRequest.text)

        XSTSErrors = {
            "2148916233": "This account does not have an xbox account",
            "2148916235": "Xbox live is not available in this account's region",
            "2148916236": "This account needs adult verification",
            "2148916237": "This account needs adult verification",
            "2148916238": "This is a child account and must be added to a Family by an adult before signing in",
        }

        if "XErr" in XSTSDict.keys():
            self.status = 1
            self.error = XSTSErrors[XSTSDict["XErr"]]
            return

        XSTSToken = XSTSDict["Token"]

        ### GETTING MINECRAFT TOKEN

        mcAuthData = {
            "identityToken": f"XBL3.0 x={xboxUhs};{XSTSToken}",
            "ensureLegacyEnabled": "true",
        }

        mcRequest = requests.post(
            url="https://api.minecraftservices.com/authentication/login_with_xbox",
            json=mcAuthData,
        )

        mcDict = json.loads(mcRequest.text)
        mcToken = mcDict["access_token"]

        ### CHECKING IF THE ACCOUNT OWNS MINECRAFT

        authHeader = {"Authorization": f"Bearer {mcToken}"}

        gameOwnedRequest = requests.get(
            url="https://api.minecraftservices.com/entitlements/mcstore",
            headers=authHeader,
        )

        gameOwnedDict = json.loads(gameOwnedRequest.text)

        #### Need to eventually decode JWT values and check against Mojang servers public key

        if gameOwnedDict["items"] == None:
            print(
                "This account does not own minecraft according to the minecraft store"
            )

        ### GETTING PROFILE INFORMATION

        profileRequest = requests.get(
            url="https://api.minecraftservices.com/minecraft/profile",
            headers=authHeader,
        )

        profileDict = json.loads(profileRequest.text)

        if "error" in profileDict.keys():
            self.status = 1
            self.error = {
                "reason": "This account's minecraft profile doesn't exist",
                "errorType": f'"{profileDict["errorType"]}"',
                "error": f'"{profileDict["error"]}"',
                "errorMessage": f'"{profileDict["errorMessage"]}"',
                "developerMessage": f'"{profileDict["developerMessage"]}"',
            }
            return

        self.authtoken = mcToken
        self.username = profileDict["name"]
        self.uuid = profileDict["id"]
        self.status = 0


if __name__ == "__main__":
    email, password, type = (
        input("Username: "),
        input("Password: "),
        input("Account Type: "),
    )
    auth = authenticate(email=email, password=password, accounttype=type)
