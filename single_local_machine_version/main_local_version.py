#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
import os
import logging
import threading


# In[ ]:


def install_required_packages():
#     sudo pip install flask
#     pip install flask-restful
    # pip3 install flask-restful
    pass




import os                                                                       
from multiprocessing import Pool                                                
                                                                                
                                                                                
processes = ('front_server_runner_local.py', 'catalog_server_runner_local.py', 'order_server_runner_local.py')                                    
                                                  
                                                                                
def run_process(process):                                                             
    os.system('python {}'.format(process))                                       
                                                                                
                                                                                
pool = Pool(processes=3)                                                        
pool.map(run_process, processes)   

