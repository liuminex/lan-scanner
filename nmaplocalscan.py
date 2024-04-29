#run with $ sudo python3 nmaplocalscan.py

from tkinter import *
import subprocess as sp
import random

matched = {}
matched['addresses'] = '[This Device]' # do not change this


# example:
matched['12:34:56:78:12:34'] = 'My Mobile Phone'

network = '192.168.1.1/24'

#FUNCTIONS

retstore=[]
i=2

def printRet():
	global i
	global retstore
	print('getting...')
	output = sp.getoutput('sudo nmap -sn '+network)
	#output="loading...";

	ret = []	
	ready =  0
	out = output.split(" ")
	scan = []
	for s in out:
		if s == 'for':
			ready = 1
			continue
		if ready == 1:
			scan.append(s)
		if ready > 0:
			ready = ready + 1
		if ready == 9:
			scan.append(s)
			lbl = 'unknown'
			if scan[1] in matched:
				lbl = matched[scan[1]]
			scan.append(lbl)
			ret.append(scan)
			scan = []
			ready = 0

	color = ["#"+''.join([random.choice('0123456') for j in range(6)])]
	for v in ret:
		found = False
		for old in retstore:
			if old[0] == v[0]:
				found = True
				break
		if not found:
			retstore.append(v)
			local_ip, mac_addr, default_name = v
			td1 = Label(root, text=local_ip,fg=color)
			td2 = Label(root, text=mac_addr,fg=color)
			td3 = Label(root, text=default_name,fg=color)
			td1.grid(row=i,column=0,padx=10,pady=5)
			td2.grid(row=i,column=1,padx=10,pady=5)
			td3.grid(row=i,column=2,padx=10,pady=5)
			i+=1

	for n in ret:
		print(n[0], n[1], n[2])
	status.config(text='--')

def refresh():
	status.config(text='loading...')
	printRet()


#DRIVER

root = Tk()

status = Label(root, text="press refresh to start")
status.grid(row=0,column=1)

thead1 = Label(root, text="IP")
thead2 = Label(root, text="MAC")
thead3 = Label(root, text="NAME")
thead1.grid(row=1,column=0,padx=10,pady=5)
thead2.grid(row=1,column=1,padx=10,pady=5)
thead3.grid(row=1,column=2,padx=10,pady=5)

refreshBtn = Button(root, text="refresh", command=refresh)
refreshBtn.grid(row=0,column=0)

printRet()

root.mainloop()

#print("\nfrom:\n",output)
