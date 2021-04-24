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


class Cache:

    def checks_in_memory_cache(self):
        return
    def save_in_memory_cache(self,request,response):
        """we cach data by saving data in memory"""
        return
    def cache.cache_consistency(request,response):
        """we need to update the cache in order to have consistency"""
    return
class Load_balancer:
    def load_balancing_algorithm(self):
        """ takes each incoming request and sends it to one of the replicas"""
        return server


# In[ ]:



@app.route('/', methods=['GET'])
def lookup():
   """allows the user to specify a topic and returns all entries belonging to that category (a title and an item number are displayed for each match)."""
   if response_from_cache = cache.checks_in_memory_cache():
       """we can resolve this request from the cache"""
       return response_from_cache
   else:
       response = load_balancer.load_balancing_algorithm()

       cache.save_in_memory_cache(request,response)
       return response
   
@app.route('/<int:id>', methods=['GET'])
def query_records(id):
   response = load_balancer.load_balancing_algorithm()
   
   cache.in_memory_cache(request,response)
   return response

@app.route('/<string:topic>', methods=['GET'])
def search(topic):
   """allows the user to specify a topic and returns all entries belonging to that category (a title and an item number are displayed for each match)."""
   response = load_balancer.load_balancing_algorithm()
   
   cache.in_memory_cache(request,response)
   return response

@app.route('/', methods=['PUT'])
def create_record():
   
   response = load_balancer.load_balancing_algorithm()
   cache.cache_consistency(request,response)
   cache.in_memory_cache(request,response)
   return response
   

   
@app.route('/<int:id>', methods=['DELETE'])
def buy(id):
   """specifies an item number for purchase."""
   response = load_balancer.load_balancing_algorithm()
   cache.cache_consistency(request,response)
   cache.in_memory_cache(request,response)
   return response

@app.route('/', methods=['POST'])
def update_record():
   response = load_balancer.load_balancing_algorithm()
   cache.cache_consistency(request,response)
   cache.in_memory_cache(request,response)
   return response


# In[ ]:



if __name__ == "__main__":
    server_IP = sys.argv[1]
    catalog_server_URL = "http://"+sys.argv[2]+":5000/"
    order_server_URL = "http://"+sys.argv[3]+":5000/"
    print("running front end microservice..........")
    app.run(host=server_IP, port=5000)

