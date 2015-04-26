# Don't touch my bin!

This uses the stem API for connect through Tor and the request library for fetching the file, both these can be installed via pip(pip install stem request).


To download all the fingerprints: 

$ curl -s https://check.torproject.org/exit-addresses | grep ExitNode  | sed 's/ExitNode //g' > fp.txt
