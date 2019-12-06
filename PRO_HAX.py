from PIL import ImageGrab
import win32gui, win32ui, win32con, win32api
import time, datetime
from desktopmagic.screengrab_win32 import (
	getDisplayRects, saveScreenToBmp, saveRectToBmp, getScreenAsImage,
	getRectAsImage, getDisplaysAsImages)

from bs4 import BeautifulSoup
import requests
import pytesseract
import cv2
import pyautogui
import pyperclip
import pickle
import re

def selectAllPaste():
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    return pyperclip.paste()



toplist, winlist = [], []
def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
win32gui.EnumWindows(enum_cb, toplist)

wordlist = {}
filename = 'wordlistFinal.pickle'
with open(filename, 'rb') as handle:
    wordlist = pickle.load(handle)

masterArr = [[] for x in range(30)]
# print(masterArr)
for k in wordlist.keys():
    # print(k)
    masterArr[len(k)].append((k,wordlist[k]))


# sort by most common occurence (second index is occurence)
for x in masterArr:
    x.sort(key=lambda x : x[1], reverse=True)

print(masterArr)

firefox = [(hwnd, title) for hwnd, title in winlist if 'firefox' in title.lower()]

hwin = firefox[0]

skribNotFound = True;
while(skribNotFound):
    print("waiting for skrib")
    toplist, winlist = [], []
    win32gui.EnumWindows(enum_cb, toplist)

    firefox = [(hwnd, title) for hwnd, title in winlist if 'firefox' in title.lower()]
    for x in firefox:
        if x[1].startswith("skribbl.io"):
            print("skribble detected!")
            hwin = x[0]
            skribNotFound = False;
            break;
    time.sleep(1)

win32gui.SetForegroundWindow(hwin)
bbox = win32gui.GetWindowRect(hwin)

while(True):
    currWord = input("Enter word:")
    wordsOfLen = masterArr[len(currWord)]
    print(wordsOfLen)
    regex = re.compile(currWord.replace("_", "."))
    newlist = list(filter(lambda x: regex.match(x[0]), wordsOfLen))

    print(newlist)