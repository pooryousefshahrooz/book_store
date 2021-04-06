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
        server_name = server_name.replace('\n','')
        server_name = server_name.replace('\t','')   
        server_IP = server_IP.replace('"', '')
        server_IP = server_IP.replace('"', '')
        server_IP = server_IP.replace('\n','')
        server_IP = server_IP.replace('\t','')  
        each_server_IP[server_name]= server_IP
print("going to run catalog server")
server_IP = each_server_IP['catalog']
os.system('scp  catalog_microservice.py -e ssh '+server_IP+':')
os.system('scp  items_warehouse_file.csv -e ssh '+server_IP+':')
os.system('ssh '+server_IP+'  python3 catalog_microservice.py '+each_server_IP["catalog"])

