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
server_IP = each_server_IP['front']

os.system('scp front_end_tier_microservice.py -e ssh '+server_IP+':')
os.system('ssh '+server_IP+'  python3 front_end_tier_microservice.py '+each_server_IP["front"]+" "+each_server_IP["catalog"]+" "+each_server_IP["order"])

