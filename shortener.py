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
    """Web application for managing shortered URLS.

    PONER COMENTARIOS

    Content is stored in a dictionary, which is initialized
    with the web content.
    The client can accest the content or add new content"""

    content: dict = {}

    def parse(self, request):
        """Return:
            1) the method of the request (POST or GET)
            2) the resource name (including /)
            3) the body of the request
            CAMBIAR COMENTARIOS
        """

        method = request.split(' ', 2)[0]
        resource = request.split(' ', 2)[1]
        index = request.find('\r\n\r\n') + len('\r\n\r\n')
        body = request[index:]

        return method, resource, body

    def format_urls(self) -> str:
        text: str = ""
        for url in self.content:
            text = text + '<br>' + self.content[url] + ' <b>as</b> ' + url
        return text

    def process(self, parsedRequest):

        (method, resource, body) = parsedRequest

        if method == "GET":
            if resource == "/":
                httpCode = "200 OK"
                htmlBody = '<html><body><form action="/" method="POST">'\
                           + '<ul><li>Type original URL: <input name="url" type=text />'\
                           + '<li>Type shorted URL: <input name="short" type="text" />'\
                           + '<input type="submit" value="Submit" /></ul>' \
                           + '<p><b>' + 'Shortered urls:' + '</b></p>' \
                           + '<p>' + self.format_urls() + '</p>'\
                           + '</form></body></html>'

            elif resource in self.content:
                httpCode = "308 Permanent Redirect"
                htmlBody = '<meta http-equiv="refresh" content="1;URL=' + self.content[resource] + '">'

            else:
                httpCode = "404 Not Found"
                htmlBody = "Error: " + resource + " is not an avaliable resource"

        if method == "POST":
    
            if body.find('url=') != -1 and body.find('&') != -1 and body.find('short=') != -1:

                info = body.split('&')
                url = unquote(info[0].split('=')[1])
                short_url = '/' + info[1].split('=')[1]

                if not url.startswith('http://') and not url.startswith('https://'):
                    url = 'https://' + url

                self.content[short_url] = url

            httpCode = "200 OK"
            htmlBody = '<html><body><a href="' + self.content[short_url] + '">' + url + '</a> is now '\
                                            + '<a href="' + self.content[short_url] + '">' + short_url + '</body></html>'

        return (httpCode, htmlBody)

if __name__ == "__main__":
    testShortener = Shortener("localhost", 1234)
