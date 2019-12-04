import pyautogui
import pyperclip
import time
import pickle

def exportReadable():
    d = {}
    with open('wordlistFinal.pickle', 'rb') as handle:
        d = pickle.load(handle)
    readable = open("wordlistReadable.txt", "w")


    for x in d.keys():
        entry = str(x) +","+ str(d[x])
        readable.write(entry+'\n')

    readable.close()

exportReadable()
# text = open("mainscreen.txt").read().split()
# print(text)
# paste = pyperclip.paste().split()
# print(paste)
# print(text[0:14] == paste[0:14])
# while(True):
#     print(pyautogui.position())
#     time.sleep(.5)
# d = {}
# with open('wordlist.pickle', 'rb') as handle:
#     d = pickle.load(handle)
# for x in d.keys():
#     d[x] = 0
# print(d)
# with open('wordlistFinal.pickle', 'wb') as handle:
#     pickle.dump(d, handle, protocol=pickle.HIGHEST_PROTOCOL)