from PIL import ImageGrab
import win32gui, win32ui, win32con, win32api
import time
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
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

#
# url="https://skribbl.io/"
# html_content = requests.get(url).text
# soup = BeautifulSoup(html_content)
# print(soup.prettify()) # print the parsed data of html
# div = soup.find('div', id='currentWord')
# print("AHHHHH",div.contents)
#

toplist, winlist = [], []
def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
win32gui.EnumWindows(enum_cb, toplist)

firefox = [(hwnd, title) for hwnd, title in winlist if 'firefox' in title.lower()]
# just grab the hwnd for first window matching firefox

hwin = firefox[0]

skribNotFound = True;
while(skribNotFound):
    print("waiting for skrib")
    toplist, winlist = [], []
    win32gui.EnumWindows(enum_cb, toplist)

    firefox = [(hwnd, title) for hwnd, title in winlist if 'firefox' in title.lower()]
    # print(firefox)
    for x in firefox:
        if x[1].startswith("skribbl.io"):
            print("skribble detected!")
            hwin = x[0]
            skribNotFound = False;
            break;
    time.sleep(1)


win32gui.SetForegroundWindow(hwin)
bbox = win32gui.GetWindowRect(hwin)
# wordlist = open("wordlist.txt", "w+")
# while(noKey):
img = getRectAsImage(bbox)
img.save("full.png")
# img = getRectAsImage()
cv2img = cv2.imread("full.png")

# hsv = cv2.cvtColor(cv2img, cv2.COLOR_BGR2HSV)
# greenmask = cv2.inRange(hsv, (36, 0, 0), (60, 255,255))
# cv2.imshow("gray", greenmask)
# cv2.waitKey(0)

# gray = cv2.cvtColor(cv2img, cv2.COLOR_BGR2GRAY)
# gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
# cv2.imshow("gray", gray)
# cv2.waitKey(0)
# text = pytesseract.image_to_string(greenmask)

wordlist = {}

with open('wordlist.pickle', 'wb') as handle:
    pickle.dump(wordlist, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('wordlist.pickle', 'rb') as handle:
    wordlist = pickle.load(handle)


text = selectAllPaste()
lines = text.split("\n")
for x in lines:
    if x.startswith("The word was"):


