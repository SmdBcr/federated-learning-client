#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 21:07:32 2020

@author: aytunctunay
"""

from kafka import KafkaConsumer
import sys
bootstrap_servers = ['185.188.130.34:9092']
topicName = 'serverdemo'
consumer = KafkaConsumer (topicName, group_id = 'servertest',bootstrap_servers = bootstrap_servers,
auto_offset_reset = 'earliest')

from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import numpy as np


import h5py




import requests 




URL_h5_client1 = "https://elasticbeanstalk-eu-central-1-335189602832.s3.eu-central-1.amazonaws.com/model/client1.h5"
URL_h5_client2 = "https://elasticbeanstalk-eu-central-1-335189602832.s3.eu-central-1.amazonaws.com/model/client2.h5"
URL_send = 'http://185.188.130.34:5000/api/federated/models/send/updated'
URL_send_json = 'http://185.188.130.34:5000/api/federated/models/send/model'





def getUpdatedWeights1(get_url):
    r = requests.get(url = get_url )
    f = open('C:\\Users\\MBICER14\\Desktop\\demo\\client1.h5', 'wb')
    f.write(r.content)
    f.close()
def getUpdatedWeights2(get_url):
    r = requests.get(url = get_url )
    f = open('C:\\Users\\MBICER14\\Desktop\\demo\\client2.h5', 'wb')
    f.write(r.content)
    f.close()
def sendWeights(get_url):
    files = {'file': open('second_client_model_weights.h5', 'rb')}
    requests.post(get_url, files=files)
    
def sendModel(get_url):
    files = {'file': open('model.json', 'rb')}
    requests.post(get_url, files=files)
    
   



model=Sequential()
model.add(Dense(11,input_dim=11,bias_initializer='uniform',activation='relu'))
model.add(Dense(8,bias_initializer='uniform',activation='relu'))
model.add(Dense(8,bias_initializer='uniform',activation='relu'))
model.add(Dense(8,bias_initializer='uniform',activation='relu'))
model.add(Dense(1,bias_initializer='uniform',activation='sigmoid'))




model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)

checkInitial = True
loopCount = 1;









try:
    for message in consumer:
        print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,message.value))
        if (str(message.value, 'utf-8') == 'update'):
            print('got it')
            if(checkInitial):
                print("Model sending the clients..")
                sendModel(URL_send_json)    
                print("Model sended!")
                checkInitial = False
            else:
                print("ROUND : " + str(loopCount))
                loopCount +=1
                print("----------------------------------------------------------------------")
                print("Updated weights from client-1 getting from the server..")
                getUpdatedWeights1(URL_h5_client1)
                print("Updated weights from client-2 getting from the server..")
                getUpdatedWeights2(URL_h5_client2)
                print("Updated weights obtained!")
                print("----------------------------------------------------------------------")        
                # load first_client_json and create model
                json_file = open('model.json', 'r')
                client_1 = json_file.read()
                json_file.close()
                client_1_model = model_from_json(client_1)
                # load second_client_json and create model
                json_file = open('model.json', 'r')
                client_2 = json_file.read()
                json_file.close()
                client_2_model = model_from_json(client_2)
        
                # load weights into first client model
                client_1_model.load_weights("client1.h5")
        
                # load weights into second client model
                client_2_model.load_weights("client2.h5")
                print("----------------------------------------------------------------------")
        
        
        
        
                models = [client_1_model , client_2_model]
                weights = [model.get_weights() for model in models]
        
                new_weights = list()
        
                for weights_list_tuple in zip(*weights):
                    new_weights.append(
                        [np.array(weights_).mean(axis=0)\
                            for weights_ in zip(*weights_list_tuple)])
            
        
            
                # load json and create model
                json_file = open('model.json', 'r')
                updated_model_json = json_file.read()
                json_file.close()
                updated_model = model_from_json(updated_model_json)
                
                updated_model.set_weights(new_weights)
        
                updated_model.save_weights("updated_model.h5")
        
        
                print("Saved updated_model to disk")
        
        
                print("----------------------------------------------------------------------")
                print("Weights sending the clients..")
                sendWeights(URL_send)
                print("Weights sended!")
            
            
            
                  
except KeyboardInterrupt:
    sys.exit() 