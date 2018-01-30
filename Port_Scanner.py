from socket import *
from queue import Queue
import time
import threading
import os
import subprocess

ips = ['google.com']
lock = threading.Lock()

def threader():
    while (True):
        thread = q.get()
        Scan_Ports(thread)
        q.task_done()

def Scan_Ports(port):
        #global ip
        #client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client = socket(AF_INET, SOCK_STREAM)
        #print('Scanning port : {} on {}'.format(port, ip))
        client.settimeout(1)
        try: 
            Port_Test = client.connect_ex((ip, port))
            
            if Port_Test == 0:
                with lock:
                    print('Port {} open on {}.'.format(port, ip))
            #client.shutdown(socket.SHUT_RDWR)
            client.close()
        
        except ConnectionRefusedError:
            print('Port {} on {} is closed'.format(port,ip))
            client.close()
        #except timeout:
        #    print('Timed out during connection')
        #    client.close()

def Target_Online(ip):
    #ensure target is online
    process = subprocess.Popen(
            ['ping', '-t', '200' ,'-i' '1', '-c' ,'5', ip],
            stdout=subprocess.DEVNULL)
    process.wait()

    if process.returncode == 0:
        print('{} is online'.format(ip))
        return True
    else:
        print('{} is offline.\nContinuing...'.format(ip))
        return False

q = Queue()
start = time.time()

global ip
for ip in ips:
    
    if not Target_Online(ip):
        continue

    #range= how many threads are being used
    for x in range(256):
        t = threading.Thread(target= threader)
        t.daemon = True
        t.start()
    
    #range= ports to be scanned
    for thread in range(1,10000):
        q.put(thread)
        
    q.join()

    print('{} has been scanned.'.format(ip))

print('Time Taken: {}'.format(time.time() - start))
