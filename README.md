

$ curl -s https://check.torproject.org/exit-addresses | grep ExitNode  | sed 's/ExitNode //g' > fp.txt
