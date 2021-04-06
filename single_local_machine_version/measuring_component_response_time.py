#!/usr/bin/env python
# coding: utf-8

# In[ ]:



import json
import logging
import requests
import sys
import os
import random
import time
import csv


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
front_end_server_URL = 'http://'+each_server_IP['front']+":5000/"



request_types = ['GET','PUT','DELETE']

end_to_end_response_time_results = 'end_to_end_response_time_results.csv'
for i in range(1000):
    time.sleep(3)
    random_number = random.randint(0,len(request_types)-1)
    request_type = request_types[random_number]
    start= round(time.time() * 1000)
    if request_type=='GET':
        response = requests.get(front_end_server_URL, data={}, headers={})
        response = response.content
    elif request_type =='PUT':
        headers = {"Content-Type": "application/json"}
        data ='{"$topic":"testing","$cost":24,"$number":2, "$title": "Post Title"}'
        response = requests.put(front_end_server_URL, data=data, headers=headers)
        
    elif request_type =='DELETE':
        random_item_number = random.randint(1,4)
        response = requests.delete(front_end_server_URL+"/"+str(random_item_number), data={}, headers={})

    end =  round(time.time() * 1000)
    E_to_E_time = end - start
    print("end to end response time for %s th request (type: %s) was %s"%(i,request_type,E_to_E_time))
    with open(end_to_end_response_time_results, 'a') as newFile:
        newFileWriter = csv.writer(newFile)
        newFileWriter.writerow([request_type,str(E_to_E_time)]) 


    

