#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
import os
import logging
import threading


# In[ ]:


# each_server_IP = {"front":'155.98.38.69',
#                  "catalog":'155.98.38.104',
#                  "order":'155.98.38.156'}
each_server_IP = {}
each_server_IP_file = open('each_server_IP.txt', "r")
for line in each_server_IP_file:
    if line:
        server_name = line.split(",")[0]
        server_IP = line.split(",")[1]
        server_port = line.split(",")[2]
        server_name = server_name.replace('\n','')
        server_name = server_name.replace('\t','')   
        server_IP = server_IP.replace('"', '')
        server_IP = server_IP.replace('"', '')
        server_IP = server_IP.replace('\n','')
        server_IP = server_IP.replace('\t','') 
        server_port = server_port.replace('"', '')
        server_port = server_port.replace('"', '')
        server_port = server_port.replace('\n','')
        server_port = server_port.replace('\t','') 
        try:
            each_server_IP[server_name].append(server_IP+','+server_port)
        except:
            each_server_IP[server_name] = [server_IP+','+server_port]
print("going to run catalog server")
# server_IP = each_server_IP['catalog']
# os.system('scp  catalog_microservice.py -e ssh '+server_IP+':')
# os.system('scp  items_warehouse_file.csv -e ssh '+server_IP+':')
# os.system('ssh '+server_IP+'  python3 catalog_microservice.py '+each_server_IP["catalog"])



def run_catalog_server_replica(server_IP,port):
    print("running catalog server iP address ",server_IP)
    #t = threading.currentThread()
#     server_IP = each_server_IP['order']
#     os.system('scp  order_microservice.py -e ssh '+server_IP+':')
    os.system('python3 catalog_microservice.py '+server_IP+' '+port)
    
print("these are each_server_IP ",each_server_IP)
for server,IP_addresses in each_server_IP.items():
    if server=='catalog':
        
        for q1,q2 in zip(*[iter(IP_addresses)] * 2):
            IP1 = q1.split(',')[0]
            port1 = q1.split(',')[1]
            t1 = threading.Thread(target=run_catalog_server_replica, args=(IP1,port1))
            #t1.setDaemon(True)
            t1.start()
            IP2 = q2.split(',')[0]
            port2 = q2.split(',')[1]
            t2 = threading.Thread(target=run_catalog_server_replica, args=(IP2,port2))
            #t2.setDaemon(True)
            t2.start()
        
#         for IP_address in IP_addresses:
#             IP = IP_address.split(',')[0]
#             port = IP_address.split(',')[1]
#             t1 = threading.Thread(target=run_catalog_server_replica, args=(IP,port))
#             t1.setDaemon(True)
#             t1.start()

main_thread = threading.current_thread()
for t in threading.enumerate():
    if t is main_thread:
        continue
# logging.debug('joining %s', t.getName())
# t.join()

