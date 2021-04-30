#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, marshal, fields
from flask import  request, jsonify
import json
import requests
import sys
import os
# Initialize Flask

app = Flask(__name__)
api = Api(app)


# In[ ]:





# In[ ]:


class Cache:
    def __init__(self):
        
        self.request_dictrionary = {}
    def checks_in_memory_cache(self,request_type,parameter):
        if request_type in self.request_dictrionary:
            if parameter in self.request_dictrionary[request_type]:
                return self.request_dictrionary[request_type][parameter]
            else:
                return False
        
        return False
    def save_in_memory_cache(self,request,parameter,response):
        """we cache data by saving data in memory"""
        try:
            self.request_dictrionary[request][parameter]= response
        except:
            self.request_dictrionary[request]={}
            self.request_dictrionary[request][parameter]= response
            
        return
    def cache_consistency(self,request_type,parameter):
        """we need to update the cache in order to have consistency"""
        try:
            self.request_dictrionary[request_type][parameter] = {}
        except:
            pass
    


class Fault_toleran_server:
    
    def update_available_replicas(self,failed_replica):
        """this function remove this replica from available replicas"""
        return
    def ongoing_replica_checker(self,server_type):
        
        """this function continuesly check each replica to see if it is on or not"""
        
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
        
        if server_type =="catalog":
            candidate_catalog_servers = each_server_IP['catalog']
        else:
            candidate_catalog_servers = each_server_IP['order']
        available_replicas = []
        for each_replica in candidate_catalog_servers:
            IP = each_replica.split(",")[0]
            port = each_replica.split(",")[1]
            try:
                response = requests.get("http://"+IP+":"+port+"/"+str(4444), data={}, headers={})
                available_replicas.append(IP+":"+port)
            except:
                pass

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
            available_servers = self.fault_tolerent_object.ongoing_replica_checker("order")
            #print("************ these are available order servers ",available_servers,len(available_servers),self.index)
            if len(available_servers)==1:
                order_server_URL = "http://"+available_servers[0]+"/"
            else:
                order_server_URL = "http://"+available_servers[self.index]+"/"
            self.index+=1
            self.index = self.index %2
            return order_server_URL
            


# In[ ]:


cache = Cache()
fault_toleran_server = Fault_toleran_server()
load_balancer = Load_balancer()


# In[ ]:



@app.route('/', methods=['GET'])
def lookup():
   """allows the user to specify a topic and returns all entries belonging to that category (a title and an item number are displayed for each match)."""
   response_from_cache = cache.checks_in_memory_cache('GET','all')
   if response_from_cache:
       """we can resolve this request from the cache"""
       print("we got the data for this GET request from our in-memory cache!")
       response =  response_from_cache
   else:
       print("we do not have data for this reguest in our cache!")
       catalog_server_URL = load_balancer.round_robin_load_balancing_algorithm('GET')

       
       if request.data:
           json_data = json.loads(request.data.decode(encoding='UTF-8'))
           payload = { 'key' : 'val' }
           data = '[{"$key": 8},{"$key": 7}]'
           data = '[{"$topic": "testing"}]'
           headers = {"Content-Type": "application/json"}
           if json_data:
               constructed_paylod = {}
               quered_topic = ''
               asked_by = ''
               for key,value in json_data.items():
                   if 'topic'==key:
                       if value:
                           quered_topic = "\""+value+"\""
                           asked_by = "\""+"$"+key+"\""

                   elif 'id'==key:
                       if value:
                           asked_by = "\""+"$"+str(key)+"\""
                           quered_topic = "\""+str(value)+"\""
               constructed_paylod[asked_by] = quered_topic
               #call catalog server
               constructed_paylod = [constructed_paylod]
               constructed_paylod = str(constructed_paylod)
               constructed_paylod =constructed_paylod.replace("'", '')
               response = requests.get(catalog_server_URL, data=constructed_paylod, headers=headers)
               response = response.content
           else:
               response = jsonify({'response':'Please specifiy another %s'%(asked_by)})
       else:
           response = requests.get(catalog_server_URL, data={}, headers={})
           response = response.content
       cache.save_in_memory_cache('GET','all',response)
   return response
   
@app.route('/<int:id>', methods=['GET'])
def query_records(id):
   #print("this is front end and we got request for ",id)
   if int(id)>2021 and int(id)<4041:
       #print("just remove fromt he cache! front end server says")
       ID = id %2021
       cache.cache_consistency("GET",ID)
       return jsonify({'response':'cache updated!'})
   elif int(id)>4041:
       #print("this is a heartbeat message")
       return jsonify({'response':'alive!'})
   else:
       response_from_cache = cache.checks_in_memory_cache('GET',id)
       if response_from_cache:
           #print("we got the result for this GET request from cache")
           """we can resolve this request from the cache"""
           response =  response_from_cache
       else:
           #print("we do not have data for this request in cache")
           catalog_server_URL = load_balancer.round_robin_load_balancing_algorithm('GET')

           items_found = []
           response = requests.get(catalog_server_URL+str(id), data={}, headers={})
           record = json.loads(response.content.decode('utf-8'))
           record = record[0]
           try:
               if record["response"]=="0":
                   response ="Unfortunately we do not have enough of this item!"
           except:
               response=record
       cache.save_in_memory_cache('GET',id,response)
       return jsonify({'response':response})

@app.route('/<string:topic>', methods=['GET'])
def search(topic):
   """allows the user to specify a topic and returns all entries belonging to that category (a title and an item number are displayed for each match)."""
   name = request.args.get('name')

   payload = { 'key' : 'val' }
   headers = {}
   #call catalog server
   res = requests.get(catalog_server_URL, data=payload, headers=headers)
   return res.content
   return jsonify({'results from other microserver': res})

@app.route('/', methods=['PUT'])
def create_record():
   catalog_server_URL = load_balancer.round_robin_load_balancing_algorithm('PUT')

   try:

       my_json = request.data.decode('utf8').replace("'", '"')

       json_data = my_json
       
       json_data = json_data[0]

       json_data = json.loads(json_data)

       payload = { 'key' : 'val' }
       data = '[{"$key": 8},{"$key": 7}]'
       headers = {"Content-Type": "application/json"}
       result = []
       if json_data:
           constructed_paylod = {}
           quered_topic = ''
           asked_by = ''
           print(json_data,type(json_data))
           for key,value in json_data.items():
                   if value:
                       quered_topic = "\""+str(value)+"\""
                       asked_by = "\""+str(key)+"\""
                       constructed_paylod[asked_by] = quered_topic
           #call catalog server
           result = set(['topic','title','number','cost']) - set(constructed_paylod)
           if result:
               constructed_paylod = [constructed_paylod]
               constructed_paylod = str(constructed_paylod)
               constructed_paylod =constructed_paylod.replace("'", '')
               response = requests.put(catalog_server_URL, data=constructed_paylod, headers=headers)
               response = response.content
       else:
           response = jsonify({'response':'Please set these values %s in your request %s'%(result)})
   except ValueError:
       response = jsonify({'response':'This is not a valid request'})
   return response

   
@app.route('/<int:id>', methods=['DELETE'])
def buy(id):
   """specifies an item number for purchase."""
   order_server_URL = load_balancer.round_robin_load_balancing_algorithm('DELETE')
   #print(" we are going to delete item ",id," asking ",order_server_URL)
   try:
       if id:
           headers = {}
           #print("going to buy this in order about ",str(id))
           response = requests.delete(order_server_URL+str(id), data={}, headers=headers)
           response = json.loads(response.content.decode('utf-8'))
           
       else:
           response = jsonify({'response':'Please set a valid item number %s in your request %s'%(str(id))})
   except ValueError:
       print("ValueError",ValueError)
       response = jsonify({'response':'This is not a valid request '})

   return response

@app.route('/', methods=['POST'])
def update_record():
   catalog_server_URL = load_balancer.round_robin_load_balancing_algorithm('POST')
   #print(" we are going to POST by asking catalog ",catalog_server_URL)
   try:
       json_data = json.loads(request.data)
       #print(json_data)
       headers = {"Content-Type": "application/json"}
       result = []
       if json_data:
           constructed_paylod = {}
           quered_topic = ''
           asked_by = ''
           for key,value in json_data.items():
                   if value:
                       quered_topic = "\""+str(value)+"\""
                       asked_by = "\""+"$"+str(key)+"\""
                       constructed_paylod[asked_by] = quered_topic
           #call catalog server
           result = set(['topic','title','number','cost']) - set(constructed_paylod)
           if result:
               constructed_paylod = [constructed_paylod]
               constructed_paylod = str(constructed_paylod)
               constructed_paylod =constructed_paylod.replace("'", '')
               #print("going to put this in catalog about ",constructed_paylod)
               response = requests.put(catalog_server_URL, data=constructed_paylod, headers=headers)
               response = response.content
       else:
           response = jsonify({'response':'Please set these values %s in your request %s'%(result)})
   except ValueError:
       print("ValueError",ValueError)
       response = jsonify({'response':'This is not a valid request'})

   return response


# In[ ]:





# In[ ]:



if __name__ == "__main__":
#     server_IP = sys.argv[1]
#     catalog_server_URL = "http://"+sys.argv[2]+":5000/"
#     order_server_URL = "http://"+sys.argv[3]+":5000/"
    print("running front end microservice..........")
    
    each_server_IP = {}
    each_server_IP_file = open('each_server_IP.txt', "r")
    for line in each_server_IP_file:
        if line:
            server_name = line.split(",")[0]
            server_IP = line.split(',')[1]
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
    server_IP_port = each_server_IP['front'][0]
    
    server_IP = server_IP_port.split(",")[0]
    server_IP_port = server_IP_port.split(",")[1]
    app.run(host=server_IP, port=int(server_IP_port))

