#!/usr/bin/env python3

#Copyright 2021 Noah Panepinto
	#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
	#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
	#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from dataclasses import dataclass
import socket
import multiprocessing
import selectors
import math
import os
import sys
import pathlib
#path0 = ('/home/Noah/bin')
path1 = (str(pathlib.Path().resolve()) + '/Libs')
#sys.path.append(path0)
sys.path.append(path1)
#print(sys.path)
import NetStuff
import BlackPack

HOST = '127.0.0.1'
GAME = 65531
LIST = 65529

sel = selectors.DefaultSelector()

def LISTTHREAD(IP, PORT):
    #content = "hello there everyone! I am going to make this message longer to see if it takes up more data eventually... i wonder if this affects the total size of the header? It doesn't seem to do so but it does definitely effect the size of content, which is intended behaviour. this is a good thing because undefined behaviour almost always causes me problems when it occurs. BLAH BLAH BLAH, need to pump more data into this so that its actually longer than the header. this is a really inneficient system lmao."
    #content = 4
    content = BlackPack.BaseCard(10, "Hearts", "Ten", BlackPack.teoh)
    #content = BlackPack.AceCard("Hearts", BlackPack.aoh)
    message = NetStuff.Message.GEN(content)
    #print (message)
    if (message.Header.ContentType is BlackPack.AceCard or message.Header.ContentType is BlackPack.BaseCard):
        print (message.Content)


def GAMETHREAD(IP, PORT):
    pass

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

if __name__ == '__main__':

    #info('Main Thread')
    LIST = multiprocessing.Process(target=LISTTHREAD, args=(HOST, LIST))
    GAME = multiprocessing.Process(target=GAMETHREAD, args=(HOST, GAME))
    LIST.start()
    GAME.start()
    LIST.join()
    GAME.join()
