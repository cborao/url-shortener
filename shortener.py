#!/usr/bin/python3

"""
 Minipráctica 1: shortener.py
 Web application to short URLS and access the content

 Author: César Borao Coratinos
 Date: March 2021

 Based on "webapp class", developed by M. Gonzalez-Barahona
 & Gregorio Robles 2009-2015 (Universidad Rey Juan Carlos)

"""

import webapp
from urllib.parse import unquote

class Shortener (webapp.webApp):

    """ Web application for managing shortered URLS.

    The client introduce an original url and a shortered url.
    The application stores in a dictionary the original url and
    provide to the client a resource with the same name as the shortered url.
    The client can access this resource to get redirected to the original url or
    repeat the process.
    """

    # The dictionary where it will be stored the original urls by shorted urls keys
    content: dict = {}

    def parse(self, request):
        """Return:
            1) the method of the request (POST or GET)
            2) the resource name (including /)
            3) the body of the request
        """
        # get the method
        method = request.split(' ', 2)[0]
        # get the resource
        resource = request.split(' ', 2)[1]
        # get the body
        index = request.find('\r\n\r\n') + len('\r\n\r\n')
        body = request[index:]

        return method, resource, body

    def format_urls(self) -> str:
        """
        Format the dictionary content to a string output
        :return a string with all the shortered url and their respective original urls
        """
        text: str = ""
        for url in self.content:
            text = text + '<br>' + self.content[url] + ' <b>as</b> ' + url
        return text

    def process(self, parsedRequest):

        (method, resource, body) = parsedRequest

        if method == "GET":

            # when the petition is the root page
            if resource == "/":
                httpCode = "200 OK"
                htmlBody = '<html><body><form action="/" method="POST">'\
                           + '<ul><li>Type original URL: <input name="url" type=text />'\
                           + '<li>Type shorted URL: <input name="short" type="text" />'\
                           + '<input type="submit" value="Submit" /></ul>' \
                           + '<p><b>' + 'Shortered urls:' + '</b></p>' \
                           + '<p>' + self.format_urls() + '</p>'\
                           + '</form></body></html>'

            # when the petition is a resource inside the dictionary (previous shortered url)
            elif resource in self.content:
                httpCode = "308 Permanent Redirect"
                htmlBody = '<meta http-equiv="refresh" content="1;URL=' + self.content[resource] + '">'

            # when the petition is an unknown resource
            else:
                httpCode = "404 Not Found"
                htmlBody = "Error: " + resource + " is not an avaliable resource"

        if method == "POST":

            if body.find('url=') == -1 or body.find('&') == -1 or body.find('short=') == -1:
                return "503 Service Unavailable", "<html>Method POST not implemented without a query string</html>"

            # We extract the original url and the shorted url from the body
            info = body.split('&')
            url = unquote(info[0].split('=')[1])
            shorted = '/' + info[1].split('=')[1]

            # We check if the url was typed including 'http://', 'https://' or not
            if not url.startswith('http://') and not url.startswith('https://'):
                # if the url dont't include it, we add it to the start of the url
                url = 'https://' + url

            # We add the url at the dictionary, with the shorted url as key
            self.content[shorted] = url

            httpCode = "200 OK"
            htmlBody = '<html><body><a href="' + self.content[shorted] + '">' + url + '</a> is now '\
                                            + '<a href="' + self.content[shorted] + '">' + shorted + '</body></html>'

        return (httpCode, htmlBody)

if __name__ == "__main__":
    testShortener = Shortener("localhost", 1234)
