import urllib.request
import urllib.error
import urllib.parse
from urllib.request import HTTPHandler, HTTPSHandler
from wsgi_intercept import InterceptedHTTPConnection


class InterceptedHTTPHandler(HTTPHandler):
    """
    Override the default HTTPHandler class with one that uses the
    WSGI_HTTPConnection class to open HTTP URLs.
    """

    def http_open(self, req):
        return self.do_open(InterceptedHTTPConnection, req)

class InterceptedHTTPSHandler(HTTPSHandler):
    """
    Override the default HTTPSHandler class with one that uses the
    WSGI_HTTPConnection class to open HTTPS URLs.
    """

    def https_open(self, req):
        return self.do_open(InterceptedHTTPSConnection, req)


def install():
    handlers = [InterceptedHTTPHandler(), InterceptedHTTPSHandler()]
    # Build and install an opener that users our intercepted handler.
    opener = urllib.request.build_opener(*handlers)
    urllib.request.install_opener(opener)

def uninstall():
    urllib.request.install_opener(None)
