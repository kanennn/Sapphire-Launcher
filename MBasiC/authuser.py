import requests

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