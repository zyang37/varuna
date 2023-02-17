#!/usr/bin/python
# to be run as a background thread in worker nodes
import json
import socket
import urllib.request
import time
from datetime import datetime, timedelta

metadata_url = "http://169.254.169.254/metadata/scheduledevents?api-version=2019-01-01"
this_host = socket.gethostname()

def client(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        sock.sendall(bytes(message, 'ascii'))

def get_scheduled_events():
    data = {}
    req = urllib.request.Request(metadata_url)
    req.add_header('Metadata', 'true')
    try:
        resp = urllib.request.urlopen(req, timeout=1)
        data = json.loads(resp.read())
    except:
        pass
    return data


def handle_scheduled_events(data, ip, port):
    # for evt in data['Events']:
    #     eventid = evt['EventId']
    #     status = evt['EventStatus']
    #     resources = evt['Resources']
    #     eventtype = evt['EventType']
    #     resourcetype = evt['ResourceType']
    #     notbefore = evt['NotBefore'].replace(" ", "_")
    #     print(datetime.now())
    #     print("+ Scheduled Event. This host " + this_host + " is scheduled for " + eventtype + " not before " + notbefore)
    #     # Logic for handling event, send morph signal to master
    #     print(this_host in resources)
    #     client(ip, port, "preempt {}".format(notbefore))

    ## "%a,_%d_%b_%Y_%H:%M:%S_%Z"
    print(datetime.now())
    notbefore = datetime.now() + timedelta(seconds=3)
    notbefore = notbefore.strftime("%a,_%d_%b_%Y_%H:%M:%S_%Z") + "UTC"
    client(ip, port, "preempt {}".format(notbefore)) 

def main():
    # ip, port = "10.0.3.4", 4200       # manager IP
    ip, port = "172.17.0.2", 4200       # manager IP
    while True:
        data = get_scheduled_events()
        print("data:", data)
        handle_scheduled_events(data, ip, port)
        break
        time.sleep(5)

if __name__ == '__main__':
    main()