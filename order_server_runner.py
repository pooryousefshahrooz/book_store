#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
import os
import logging
import threading


# In[ ]:


print("going to run order server")
# each_server_IP = {"front":'155.98.38.69',
#                  "catalog":'155.98.38.104',
#                  "order":'155.98.38.156'}
each_server_IP = {}
each_server_IP_file = open('each_server_IP.txt', "r")
for line in each_server_IP_file:
    if line:
        server_name = line.split(",")[0]
        server_IP = line.split(",")[1]
        port = line.split(',')[2]
        server_name = server_name.replace('\n','')
        server_name = server_name.replace('\t','')   
        server_IP = server_IP.replace('"', '')
        server_IP = server_IP.replace('"', '')
        server_IP = server_IP.replace('\n','')
        server_IP = server_IP.replace('\t','')  
        port = port.replace('"', '')
        port = port.replace('"', '')
        port = port.replace('\n','')
        port = port.replace('\t','')  
        try:
            each_server_IP[server_name].append(server_IP+','+port)
        except:
            each_server_IP[server_name]= [server_IP+','+port]
        
def run_order_server_replica(server_IP,port):
    #t = threading.currentThread()
#     server_IP = each_server_IP['order']
#     os.system('scp  order_microservice.py -e ssh '+server_IP+':')
    print("running order server ",server_IP)
    os.system('python3 order_microservice.py '+server_IP+' '+port)
    
print("these are each_server_IP2 ",each_server_IP)

for server,IP_addresses in each_server_IP.items():
    if server=='order':
        
        for q1,q2 in zip(*[iter(IP_addresses)] * 2):
            IP1 = q1.split(',')[0]
            port1 = q1.split(',')[1]
            t1 = threading.Thread(target=run_order_server_replica, args=(IP1,port1))
            #t1.setDaemon(True)
            t1.start()
            IP2 = q2.split(',')[0]
            port2 = q2.split(',')[1]
            t2 = threading.Thread(target=run_order_server_replica, args=(IP2,port2))
            #t2.setDaemon(True)
            t2.start()
        
#         for IP_address in IP_addresses:
#             IP = IP_address.split(',')[0]
#             port = IP_address.split(',')[1]
#             t2 = threading.Thread(target=run_order_server_replica, args=(IP,port))
#             t2.setDaemon(True)
#             t2.start()

main_thread = threading.current_thread()
for t in threading.enumerate():
    if t is main_thread:
        continue
# logging.debug('joining %s', t.getName())
# t.join()


