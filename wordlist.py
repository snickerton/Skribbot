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

def selectAllPaste():
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    return pyperclip.paste()
toplist, winlist = [], []
def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
win32gui.EnumWindows(enum_cb, toplist)

wordlist = {}
with open('wordlist.pickle', 'rb') as handle:
    wordlist = pickle.load(handle)

firefox = [(hwnd, title) for hwnd, title in winlist if 'firefox' in title.lower()]
# just grab the hwnd for first window matching firefox

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
    print(datetime.datetime.now())
    win32gui.SetForegroundWindow(hwin)
    time.sleep(.1)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(.1)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(.1)

    text = pyperclip.paste()
    if text.split() == open("disconnectscreen.txt").read().split():
        # main menu screen
        print("connection lost detected")
        pyautogui.click(x=2871, y=600, clicks=1, button='left')
        time.sleep(.5)
        pyautogui.click(x=2871, y=600, clicks=1, button='left')
        time.sleep(.5)
        pyautogui.click(x=2652, y=539, clicks=1, button='left')
        time.sleep(5)
    elif text.split() == open("mainscreen.txt").read().split():
        # main menu screen
        print("mainscreen detected")
        time.sleep(.5)
        pyautogui.click(x=2652, y=539, clicks=1, button='left')
        time.sleep(5)
    else:
        print("in game...")
        lines = text.split("\r\n")
        for i,x in enumerate(lines):
            if x.startswith("Choose a word"):
                for bob in lines[i+1:i+4]:
                    if bob not in wordlist:
                        print("NEW WORD FOUND")
                        print(bob)
                        wordlist[bob] = len(bob)
            if x.startswith("The word was '"):
                word = x[14:len(x)-1]
                if word not in wordlist:
                    print("NEW WORD FOUND")
                    print(word)
                    wordlist[word] = len(word)

        print("Saving wordlist: ", str(wordlist))
        with open('wordlist.pickle', 'wb') as handle:
            pickle.dump(wordlist, handle, protocol=pickle.HIGHEST_PROTOCOL)
        time.sleep(12)
