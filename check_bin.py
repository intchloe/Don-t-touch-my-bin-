import socket
import requests
import socks
import stem.process
import hashlib
import tempfile
import os

from stem.util import term

SOCKS_PORT = 1338
file_hash = "dc8d3ab6669b0a634de3e48477e7eb1282a770641194de2171ee9f3ec970c088"

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', SOCKS_PORT)
socket.socket = socks.socksocket

def getaddrinfo(*args):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

socket.getaddrinfo = getaddrinfo

def start():
    file = open("fp.txt", mode="r")
    for line in file.readlines():
        line = line.strip()
        tor_process = None
        try:
            print("Testing " + line)
            tor_process = stem.process.launch_tor_with_config(
                config = {
                        'SocksPort': str(SOCKS_PORT),
                        'ExitNodes': line,
                        "DataDirectory": tempfile.gettempdir() + os.pathsep + str(SOCKS_PORT)
                    },
                )
            m = hashlib.sha256()
            r = requests.get("http://the.earth.li/~sgtatham/putty/latest/x86/putty.exe", timeout=15)
            if r.status_code == 200:
                m = hashlib.sha256()
                m.update(r.content)
                
            if m.hexdigest() == file_hash:
                print(term.format("Not modified for node " + line, term.Color.GREEN))
                tor_process.kill()
            else:
                print(term.format("The hashsum does not match for fingerprint " + line, term.Color.RED))
                f = open(str(line).strip('\n'), 'wb')
                f.write(r.content)
                f.close()
                tor_process.kill()

        except Exception as e:
            print(str(e))
            if not tor_process is None:
                tor_process.kill()
        if not tor_process is None:
                tor_process.kill()

    file.close()
    
if __name__ == "__main__":
    start()
