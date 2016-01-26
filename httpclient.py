#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
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
    HTTP_CONNECTION = 'Connection: keep-alive \r\n'
    HTTP_ACCEPT = 'Accept: text/html,text/plain,application/xhtml+xml,application/xml,application/json; \r\n'
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
        return None

    def get_headers(self, data=None):
        request += self.method + ' /' + self.path + self.HTTP_REQ + self.HTTP_CONNECTION + self.HTTP_ACCEPT + self.HTTP_CONTENT_TYPE

        if(self.method == "POST"):
            request += request + self.Content-Length + len(data) + self.CRLF + self.CRLF + data
        else:
            request += request + self.CRLF

        return request

    def get_body(self, data):
        return None

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
        #regex from http://stackoverflow.com/questions/27745/getting-parts-of-a-url-regex
        match = re.search('^((http[s]?|ftp):\/\/)?\/?([^\/\.]+\.)*?([^\/\.]+\.[^:\/\s\.]{2,3}(\.[^:\/\s\.]‌​{2,3})?)(:\d+)?($|\/)([^#?\s]+)?(.*?)?(#[\w\-]+)?$', url)

        if(match.group(4) is None):
            raise Exception('No hostname')
        else:
            self.host = match.group(4)

        if(match.group(6) is None):
            self.port = 80
        else:
            self.port = match.group(6)
            self.port = self.port[1:]

        if(match.group(8) is None):
            self.path = ''
        else:
            self.path = match.group(8)

        print self.host
        print self.port
        print self.path

    def GET(self, url, args=None):

        self.method = 'GET'
        self.urlParse(url)
        socket = self.connect(self.host, self.post)

        request = self.get_headers()
        socket.sendall(request)
        response = self.recvall(socket)

        code = self.get_code(response)
        body = self.get_body(response)

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        self.method = 'POST'
        code = 500
        body = ""
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
