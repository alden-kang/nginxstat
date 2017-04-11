#!/usr/local/python

import argparse
import json
import urllib3
import time

def getNginxStatus(nginxSession):

    response = nginxSession.request('GET',"/nginx_status")
    return response.data

def printError(message):

    print "[ERROR] "+message

def printHeader():

    print "%10s\t%10s\t%10s\t%10s\t%10s\t%10s\t%10s" % \
        ( "connections","accepts/s","handled/s","requests/s","reading","writing","waiting" )

def printData(perfData):

    print "%10d\t%10.2f\t%10.2f\t%10.2f\t%10d\t%10d\t%10d" % \
        (perfData['connections'], perfData['accepts'], perfData['handled'], perfData['requests'], perfData['reading'], perfData['writing'], perfData['waiting'])

def monitoringNginxStatus(nginxSession, interval):

    # Inititialize variables

    ACTIVE_CONNECTIONS=2
    ACCEPTS=7
    HANDLED=8
    REQUESTS=9
    READING=11
    WRITING=13
    WAITING=15

    line = 0

    perfData = {}

    havingPrevData = False

    printHeader()

    while(True):

        statData = getNginxStatus(nginxSession).split(' ')

        connectionsCurr = int(statData[ACTIVE_CONNECTIONS])

        acceptsCurr = int(statData[ACCEPTS])
        handledCurr = int(statData[HANDLED])
        requestsCurr = int(statData[REQUESTS])

        readingCurr = int(statData[READING])
        writingCurr = int(statData[WRITING])
        waitingCurr = int(statData[WAITING])

        if havingPrevData == True:
            perfData['connections'] = connectionsCurr

            perfData['accepts'] = float(acceptsCurr - acceptsPrev) / float(interval)
            perfData['handled'] = float(handledCurr - handledPrev) / float(interval)
            perfData['requests'] = float(requestsCurr - requestsPrev) / float(interval)

            perfData['reading'] = readingCurr
            perfData['writing'] = writingCurr
            perfData['waiting'] = waitingCurr

            if line%10 == 0 :
                print "\n"
                printHeader()

            printData(perfData)

        line = line+1
        acceptsPrev = acceptsCurr
        handledPrev = handledCurr
        requestsPrev = requestsCurr

        havingPrevData = True

        time.sleep(interval)

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--server", help="the address of nginx server (default localhost)",default="localhost", required=False)
    parser.add_argument("--port", help="the port of nginx server (default 80)", default=80, required=False)
    parser.add_argument("--interval", help="the interval of stat api request (default 1s)", default=1, required=False, type=int)

    args = parser.parse_args()

    server = args.server
    port = args.port
    interval = args.interval

    try:

        nginxSession = urllib3.HTTPConnectionPool(server, maxsize=1, port=port, timeout=10)
        nginxSession.request('GET', '/nginx_status')

    except:

        printError("nginx status is not enabled on " + server + ":" + str(port))
        exit(1)

    monitoringNginxStatus(nginxSession, interval)

if __name__ == "__main__":
    main()
