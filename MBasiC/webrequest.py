import sys
import json

# import PyQt6
from PyQt6.QtCore import QUrl, QByteArray
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineHttpRequest


class requestPage(QWebEnginePage):
    def __init__(self, url=None, method=None, headers=None, data=None) -> None:
        # Initiate the application
        self.app = QApplication(sys.argv)
        super().__init__()

        # Make sure the necessary variables aren't empty
        if url == None:
            raise ValueError("Passed url variable cannot be empty")
        if method == None:
            raise ValueError("Passed method variable cannot be empty")

        # Creates the main request variable
        self.req = QWebEngineHttpRequest()

        # Assign the variables used to setup the request later in self.setupRequest()
        self.method = method
        self.url = url
        self.headers = headers

        # Only assign this if the method is post
        if self.method == "post":
            self.postData = data

        # Setup the request
        self.setupRequest()

        # Create a new html variable and stuff, then load the request and launch the app
        self.html = ""
        self.loadFinished.connect(self.finish)
        self.load(self.req)
        self.app.exec()

    def setupRequest(self):

        # Assign the method variable
        if self.method == "get":
            method = QWebEngineHttpRequest.Method.Get
        elif self.method == "post":
            method = QWebEngineHttpRequest.Method.Post
        else:
            raise ValueError(
                "Expected 'get' or 'post' methods, but received '{}'".format(
                    self.method
                )
            )

        # Assign the method variable to the request method
        self.req.setMethod(method)
        self.req.setUrl(QUrl(self.url))

        # Assign the headers
        if self.headers != None:
            for i in self.headers:
                self.req.setHeader(
                    QByteArray(i[0].encode("ascii")),
                    QByteArray(i[1].encode("ascii")),
                )

        # Assign the postData if the method is post
        if self.method == "post":
            self.req.setPostData(bytes(json.dumps(self.postData), "utf-8"))

    # This part is a bit over my head
    def finish(self):
        self.html = self.toHtml(self.callHtml)

    def callHtml(self, html_str):
        self.html = html_str
        self.deleteLater()
        self.app.quit()


def main():
    url = "https://google.com"
    method = "get"
    page = requestPage(url, method)


if __name__ == "__main__":
    main()
