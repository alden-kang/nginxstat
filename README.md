# Nginx Status Tool

## About

You can see stats of nginx like vmstat tool.
It shows metrics of nginx stub status.

## Requirements
- python
- python urllib3

## Features
- The current number of active client connections including Waiting connections : connections
- The number of accepted client connections per second : accepts/s
- The number of handled connections per second : handled/s
- The number of client requests per second : requests/s
- The current number of connections where nginx is reading the request header : reading
- The current number of connections where nginx is writing the response back to the client : writing
- The current number of idle client connections waiting for a request : waiting

## Usage
```
usage: python ./nginxstat.py [-h] [--server SERVER] [--port PORT] [--interval INTERVAL]

optional arguments:
  -h, --help           show this help message and exit
  --server SERVER      the address of nginx server (default localhost)
  --port PORT          the port of nginx server (default 80)
  --interval INTERVAL  the interval of stat api request (default 1s)
```

## Example
```
[root@server ~]# python ./nginxstat.py --server rocket-talk-api01.s2.krane.9rum.cc --interval 1
connections	 accepts/s	 handled/s	requests/s	   reading	   writing	   waiting
       306	     42.00	     42.00	     46.00	         0	         6	       295
       313	     39.00	     39.00	     42.00	         0	         1	       307
       313	     39.00	     39.00	     36.00	         0	         1	       306
       307	     35.00	     35.00	     42.00	         0	         1	       301
       302	     42.00	     42.00	     43.00	         0	         3	       294
```

## Changelog

See the [CHANGELOG.md file](CHANGELOG.md).
