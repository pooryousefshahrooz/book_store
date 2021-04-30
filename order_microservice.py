#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, marshal, fields
from flask import  request, jsonify
import json
import logging
import requests
import sys
import os
import time
# Initialize Flask
app = Flask(__name__)
api = Api(app)


# In[ ]:


class Fault_toleran_server:
    
    def update_available_replicas(self,failed_replica):
        """this function remove this replica from available replicas"""
        return
    def ongoing_replica_checker(self,server_type):
        
        """this function continuesly check each replica to see if it is on or not"""
        #print(" we are going to get the candiate replicas")
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
                    each_server_IP[server_name]= [server_IP+','+server_port]
        candidate_catalog_servers = []
        #print("we read the line. ",each_server_IP)
        if server_type =="catalog":
            candidate_catalog_servers = each_server_IP['catalog']
        elif server_type=='order':
            candidate_catalog_servers = each_server_IP['order']
        else:
            candidate_catalog_servers = each_server_IP['front']
        available_replicas = []
        #print("these are our candiates ",candidate_catalog_servers)
        for each_replica in candidate_catalog_servers:
            IP = each_replica.split(",")[0]
            port = each_replica.split(",")[1]
            try:
                response = requests.get("http://"+IP+":"+port+"/"+str(4444), data={}, headers={})
                available_replicas.append(IP+":"+port)
            except:
                pass
        #print(' available_replicas ',available_replicas,server_type)
        return available_replicas

class Load_balancer:
    
    def __init__(self):
        self.index = 0
        self.fault_tolerent_object = Fault_toleran_server()
    def round_robin_load_balancing_algorithm(self,request_type):
        
        """ takes each incoming request and sends it to one of the replicas"""
        
        if request_type in ["GET","PUT","POST"]:
            available_servers = self.fault_tolerent_object.ongoing_replica_checker("catalog")
            if len(available_servers) ==1:
                catalog_server_URL = "http://"+available_servers[0]+"/"
            else:
                catalog_server_URL = "http://"+available_servers[self.index]+"/"
            self.index+=1
            self.index = self.index %2
            return catalog_server_URL
        else:
            available_servers = self.fault_tolerent_object.ongoing_replica_checker("catalog")
            if len(available_servers)==1:
                order_server_URL = "http://"+available_servers[0]+"/"
            else:
                order_server_URL = "http://"+available_servers[self.index]+"/"
            self.index+=1
            self.index = self.index %2
            return order_server_URL
            


# In[ ]:


fault_toleran_server = Fault_toleran_server()
load_balancer = Load_balancer()


# In[ ]:


def server_push(id):
    """this function remove the records in cache at frond end server"""
    return

@app.route('/<int:id>', methods=['GET'])
def query_records(id):
    #print("this is front end and we got request for ",id)
    if int(id)==4444:
        #print("just remove fromt he cache! front end server says")
        return jsonify({'response':'heart_beat!'})
@app.route('/<int:id>', methods=['DELETE'])
def buy(id):
            
    
    """first verify that the item is in stock by querying the catalog server and then 
    decrement the number of items in stock by one. 
    The buy request can fail if the item is out of stock."""
    
    # we add this 3 milliseconds to evaluate the benefit of caching
    
    constructed_paylod = {}
    quered_topic = ''
    asked_by = ''
    
    #print("we are in order and going to ask catalog ",catalog_server_URL,' to delete ',id)
    if id:
        if int(id) ==4444:
            return jsonify({"reponse":"heartbeat"})
        else:
            time.sleep(0.02)
            catalog_server_URL = load_balancer.round_robin_load_balancing_algorithm('DELETE')
            logging.info("request received: received request for buying item %s"%(str(id)))
            headers = {"Content-Type": "application/json"}
            constructed_paylod ={}
            asked_by = "\""+"$id\""
            quered_topic = "\""+str(id)+"\""
            constructed_paylod[asked_by] = quered_topic
            constructed_paylod = [constructed_paylod]
            constructed_paylod = str(constructed_paylod)
            constructed_paylod =constructed_paylod.replace("'", '')
            response = requests.get(catalog_server_URL+str(id), data={}, headers={})
            record = json.loads(response.content.decode('utf-8'))

            record = record[0]
            #print(type(record),record)
            try:
                if record["response"]=="0":
                    response ="We do not have enough of this item"
            except:
                constructed_paylod ={}
                asked_by = "\""+"$id\""
                quered_topic = "\""+str(id)+"\""
                constructed_paylod[asked_by] = quered_topic
                #call catalog server
                constructed_paylod = [constructed_paylod]
                constructed_paylod = str(constructed_paylod)
                constructed_paylod =constructed_paylod.replace("'", '')
                #print("we have this item in catalog let decrease it by askin the catalog to do that for us ",constructed_paylod)
                response = requests.post(catalog_server_URL, data=constructed_paylod, headers=headers)
                record = json.loads(response.content.decode('utf-8'))
                record = record[0]
                if record["response"]=="1":
                    response ="Item numbers was decreased on the database sucessfully"
                    server_push(id)
                elif record["response"]=="0":
                    response ="We do not have enough of this item"
                elif record["response"]=="-1":
                    response ="Unfortunately we do not have this item"
                elif record["response"]=="-2":
                    response ="This is not a valid request"
    else:
        response ="This is not a valid request"
        logging.info("request received: This is not a valid request ")
    if int(id)<4444:
        logging.info("request processed: received request for buying item %s processed"%(str(id)))
        #print("we asked catalog for deleting ",catalog_server_URL,response)
        #fault_toleran_server = Fault_toleran_server()
        available_catalog_servers  = fault_toleran_server.ongoing_replica_checker("catalog")
        #print("we will update these catalog servers ",available_catalog_servers,id)
        for catalog_server in available_catalog_servers:
            if catalog_server not in catalog_server_URL:
                response2 = requests.get("http://"+catalog_server+"/"+str(2021+id), data={}, headers={})
        available_front_end_servers = fault_toleran_server.ongoing_replica_checker("front")
        #print("these are fronts ",available_front_end_servers,id)
        for fron_end_server in available_front_end_servers:
            if fron_end_server not in catalog_server_URL:
                #print("we are going to ask front end to remove this from cache ",fron_end_server+"/"+str(2021+id))
                response2 = requests.get("http://"+fron_end_server+"/"+str(2021+id), data={}, headers={})
        #print("we removed from cache of front end")
        return jsonify({"reponse":response})


# In[ ]:


order_log_file = 'orderserver_log_file.log'
logging.basicConfig(filename=order_log_file, filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)
if __name__ == "__main__":
    server_IP = sys.argv[1]
    server_port = sys.argv[2]
    #catalog_server_URL = "http://"+sys.argv[2]+":5000/"
    print("running order microservice..........",server_IP)
    logging.info("running order microservice..........")
    app.run(host=server_IP, port=int(server_port))

