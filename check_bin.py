import socket
import requests
import socks
import stem.process
import hashlib, os

from stem.util import term

SOCKS_PORT = 1338
putty_hash = "dc8d3ab6669b0a634de3e48477e7eb1282a770641194de2171ee9f3ec970c088"

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', SOCKS_PORT)
socket.socket = socks.socksocket

def getaddrinfo(*args):
  return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

socket.getaddrinfo = getaddrinfo

def read_fingerprints():
    with open("fp.txt", mode="r") as fingerprints:
        for line in fingerprints:
            try:
                tor_process = stem.process.launch_tor_with_config(
                    config = {
                    'SocksPort': str(SOCKS_PORT),
                    'ExitNodes': str(line),
                      },
                    )
                print "testing %s..." %line.strip('\n')
                m = hashlib.sha256()
                r = requests.get("http://the.earth.li/~sgtatham/putty/latest/x86/putty.exe", timeout=15)
                if r.status_code == 200:
                        m = hashlib.sha256()
                        m.update(r.content)
                if m.hexdigest() == putty_hash:
                        print term.format("Not modified for FP %s", term.Color.GREEN) %line
                        tor_process.kill()
                else:
                        print term.format("The hashsum does not match!! for FP %s", term.Color.RED) %line
                        f = open(str(line).strip('\n'), 'wb')
                        f.write(r.content)
                        f.close()
                        tor_process.kill()

            except:
                tor_process.kill()
            continue
            tor_process.kill()

read_fingerprints()
