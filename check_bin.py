import socket
import requests
import socks
import stem.process
import hashlib
import tempfile
import os
import argparse

from stem.descriptor.remote import DescriptorDownloader
from stem.util import term

argparse = argparse.ArgumentParser()
argparse.add_argument("-f", "--file", dest = "filepath", help = "File path")
argparse.add_argument("-u", "--url", dest = "url", help = "URL to download through nodes")
args = argparse.parse_args()

global file
file = args.filepath

global file_hash

if not file is None:
    m = hashlib.sha256()
    fis = open(file)
    m.update(fis.read())
    fis.close()
    file_hash = m.hexdigest()
else:
    file_hash = "dc8d3ab6669b0a634de3e48477e7eb1282a770641194de2171ee9f3ec970c088"

print("SHA256 sum: " + file_hash)

global url
url = args.url or "http://the.earth.li/~sgtatham/putty/latest/x86/putty.exe"

if url.startswith("https://"):
    print(term.format("Detected HTTPS connection, should be plaintext (HTTP)", term.Color.RED))

print("URL: " + url)

SOCKS_PORT = 1330
TIMEOUT = 10

downloader = DescriptorDownloader(
  use_mirrors = False,
  timeout = 10,
)

query = downloader.get_server_descriptors()

for desc in downloader.get_server_descriptors():
        if desc.exit_policy.is_exiting_allowed():
                file = open("fp.txt", "a")
                file.write('{}\n'.format(desc.fingerprint))
                file.close()

xlines = sum(1 for line in open('fp.txt'))
print("We will test " + str(xlines) + "nodes")
atline = 0

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
        global atline
        atline += 1

        try:
            print("Testing " + str(line) + " [" + str(atline) + " of " + str(xlines) + " tested]")
            tor_process = stem.process.launch_tor_with_config(
                config = {
                        'SocksPort': str(SOCKS_PORT),
                        'ExitNodes': str(line),
                        "DataDirectory": tempfile.gettempdir() + os.pathsep + str(SOCKS_PORT)
                    },
                timeout=TIMEOUT)
            m = hashlib.sha256()
            r = requests.get(url, timeout=15)
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
