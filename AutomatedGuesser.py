from PIL import ImageGrab
import win32gui, win32ui, win32con, win32api, win32clipboard
import time, datetime
from desktopmagic.screengrab_win32 import (
	getDisplayRects, saveScreenToBmp, saveRectToBmp, getScreenAsImage,
	getRectAsImage, getDisplaysAsImages)

from bs4 import BeautifulSoup
import requests
import re
import pytesseract
import cv2
import pyautogui
import pyperclip
import pickle

def selectAllPaste():
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    return pyperclip.paste()

def getAnsList(currWord):
    print("Receiving: ", currWord)
    formattedWord = currWord.replace("-", " ")
    wordsOfLen = masterArr[len(currWord)]
    print("Word length is: ", len(currWord))
    formattedWord = formattedWord.replace("_", "[a-zA-Z]")

    regex = re.compile(formattedWord)
    newlist = list(filter(lambda x: regex.match(x[0]), wordsOfLen))
    return newlist

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


# sort by most common occurrence (second index is occurrence)
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

lastWordSaved = "N/A"
# words that have already been registered, each session is only like 20 min max so we don't have to worry about large data sizes for this
caughtWords = []
while(True):
    print(datetime.datetime.now())
    print("\t\t LAST WORD SAVED: ", lastWordSaved)
    win32gui.SetForegroundWindow(hwin)
    time.sleep(.1)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(.1)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(.1)

    text = pyperclip.paste()

    if text.split() == open("mainscreen.txt").read().split():
        # main menu screen
        print("mainscreen detected")
        caughtWords = []
        time.sleep(.5)
        pyautogui.click(x=2652, y=539, clicks=1, button='left')
        time.sleep(5)
        # arbitrary amount of first couple of words just to confirm it's a variation of the main menu screen
    elif text.split()[0:14] == open("mainscreen.txt").read().split()[0:14]:
        # main menu screen
        # x=2652, y=539 original ok button
        print("boot detected")
        # reset words that you've already seen
        caughtWords = []
        # click out the notification window a couple of times
        pyautogui.click(x=2294, y=625, clicks=1, button='left')
        time.sleep(.1)
        pyautogui.click(x=2294, y=625, clicks=1, button='left')
        time.sleep(.1)
        pyautogui.click(x=2294, y=625, clicks=1, button='left')
        time.sleep(.3)
        pyautogui.click(x=2294, y=625, clicks=1, button='left')
        time.sleep(.5)
        pyautogui.click(x=2652, y=539, clicks=1, button='left')
        time.sleep(5)
    else:
        print("in game...")

        win32gui.SetForegroundWindow(hwin)
        pyautogui.hotkey('escape')
        win32clipboard.OpenClipboard()
        word = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()

        ansList = getAnsList(word)
        print(ansList)
        if len(ansList) == 1:
            win32clipboard.OpenClipboard()
            win32clipboard.SetClipboardText(ansList[0][0])
            win32clipboard.CloseClipboard()
            print("copied answer to clipboard")

        lines = text.split("\r\n")
        for i,x in enumerate(lines):
            if x.startswith("Choose a word"):
                for bob in lines[i+1:i+4]:
                    if bob not in wordlist:
                        lastWordSaved = "New word found: " + bob + " | " + str(datetime.datetime.now())
                        print(lastWordSaved)
                        wordlist[bob] = 0
                        # wordlist[bob] = len(bob)
            if x.startswith("The word was '"):
                word = x[14:len(x)-1]
                if word not in caughtWords:
                    lastWordSaved =  word + " | " + str(datetime.datetime.now())
                    print("New word found: " + lastWordSaved)
                    wordlist[word] = wordlist.get(word, 0) + 1
                    print("\tPrev Count: ",wordlist[word]-1, " | New Count: ", wordlist[word])
                    caughtWords.append(word)

        formattedList = [(k, wordlist[k]) for k in wordlist.keys()]
        formattedList.sort(key=lambda x:x[1],reverse=True)

        print("Saving to ",filename, ": ", str(formattedList))
        with open(filename, 'wb') as handle:
            pickle.dump(wordlist, handle, protocol=pickle.HIGHEST_PROTOCOL)
        time.sleep(12)
