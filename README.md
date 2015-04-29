# Don't touch my bin

This uses the stem API for connecting through Tor and the request library for fetching the file, both these can be installed via pip(pip install stem request).


To download all the fingerprints: 

```
$ curl -s https://check.torproject.org/exit-addresses | grep ExitNode  | sed 's/ExitNode //g' > fp.txt
```

Defaults to download PuTTY if no URL is specified, and latest PuTTY hash if no file is specified

## Synopsis

```
$ python3 check_bin.py [-f | --file <path>] [-u | --url <path>]
```

## Requirements

- stem, request (pip install stem request)

## Thanks

- https://keybase.io/likvidera
- https://github.com/redpois0n