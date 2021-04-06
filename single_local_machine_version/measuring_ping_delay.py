#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
from time import sleep


# In[ ]:


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




def ping(server_IP):
    online = os.system("ping -c 10 "+server_IP)
    if(online == 0):
        print("Avilabe with ",online)
        return True
    else:
        print("Ofline with ",online)
        return False
ping(server_IP)
print("done")

