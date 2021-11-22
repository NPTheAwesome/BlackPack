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
import types
import os

HOST = '127.0.0.1'
SERV = 65529
GAME = 65528

THREADMAX      = multiprocessing.cpu_count()
SERVTHREADMAX  = 1#math.floor(THREADMAX / 2)
GAMETHREADMAX  = 1#math.floor(THREADMAX / 2)
SERVTHREADPOOL = multiprocessing.Pool(SERVTHREADMAX)
GAMETHREADPOOL = multiprocessing.Pool(GAMETHREADMAX)

@dataclass
class Server:
    name: str
    ip: chr
    port: int = 65532
    
sel = selectors.DefaultSelector()

ServerList = {}

def SERVTHREAD(IP, PORT):
    pass

def GAMETHREAD(IP, PORT):
    pass

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

if __name__ == '__main__':
    info('Main Thread')
    SERV = multiprocessing.Process(target=SERVTHREAD, args=(HOST, SERV))
    GAME = multiprocessing.Process(target=GAMETHREAD, args=(HOST, GAME))
    SERV.start()
    GAME.start()
    SERV.join()
    GAME.join()