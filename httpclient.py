#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):

    HTTP_REQ = ' HTTP/1.1 \r\n'
    HTTP_HOST = 'HOST: '
    HTTP_USER_AGENT = 'User-Agent: Mozilla/5.0 Chrome/48.0.2564.82 Safari/537.36\r\n'
    HTTP_CONNECTION = 'Connection: close \r\n'
    HTTP_ACCEPT = 'Accept: text/html,text/plain,text/css,application/xhtml+xml,application/xml,application/json; \r\n'
    HTTP_ACCEPT_LANG = 'Accept-Language: en-US \r\n'
    HTTP_CONTENT_TYPE = 'Content-Type: application/x-www-form-urlencoded,application/json; \r\n'
    HTTP_CONTENT_LENGTH = 'Content-Length: '
    CRLF = '\r\n'

    #def get_host_port(self,url):

    def connect(self, host, port):
        # use sockets!
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((host, port))
        return clientSocket

    def get_code(self, data):
        sections = data.split('\r\n\r\n', 1)
        header_lines = str.splitlines(sections[0])
        http_line = header_lines[0].split()
        return int(http_line[1])

    def get_headers(self, data):
        sections = data.split('\r\n\r\n', 1)
        return sections[0]

    def get_body(self, data):
        sections = data.split('\r\n\r\n', 1)
        return sections[1]

    def build_request(self, data=None):
        request = ''
        request += self.method + ' /' + self.path + self.HTTP_REQ + self.HTTP_HOST + self.host + ':' + str(self.port) + self.CRLF + self.HTTP_USER_AGENT + self.HTTP_CONNECTION + self.HTTP_ACCEPT + self.HTTP_ACCEPT_LANG

        if(self.method == "POST"):
            request += self.HTTP_CONTENT_TYPE + self.HTTP_CONTENT_LENGTH + str(len(data)) + self.CRLF + self.CRLF + data
        else:
            request += self.CRLF

        return request

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def urlParse(self, url):
        #regex based from http://stackoverflow.com/questions/27745/getting-parts-of-a-url-regex
        match = re.search('^(http[s]?:\/\/)?(([^:\/])+)(:\d+)?($|\/)([^#?\s]+)?(.*?)?(#[\w\-]+)?$', url)

        try:
            if(match.group(2) is None):
                raise Exception('No hostname')
            else:
                self.host = match.group(2)

            if(match.group(4) is None):
                self.port = 80
            else:
                self.port = match.group(4)
                self.port = int(self.port[1:])

            if(match.group(6) is None):
                self.path = ''
            else:
                self.path = match.group(6)

            if(match.group(7) is not None):
                self.path += match.group(7)

        except:
            raise Exception('Could not parse url. Not a valid url')

    def GET(self, url, args=None):

        self.method = 'GET'
        self.urlParse(url)
        request = ''
        request = self.build_request()

        socket = self.connect(self.host, self.port)
        socket.sendall(request)
        response = self.recvall(socket)

        code = self.get_code(response)
        body = self.get_body(response)

        print response

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        self.method = 'POST'
        self.urlParse(url)

        encoded_args = ''
        if(args):
            encoded_args = urllib.urlencode(args)

        request = ''
        request = self.build_request(encoded_args)

        socket = self.connect(self.host, self.port)
        socket.sendall(request)
        response = self.recvall(socket)

        code = self.get_code(response)
        body = self.get_body(response)

        print response

        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )

if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1] )
