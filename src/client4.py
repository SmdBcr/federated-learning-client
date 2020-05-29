#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 13:52:10 2020

@author: aytunctunay
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 13:27:38 2020

@author: aytunctunay
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 21:01:47 2020

@author: aytunctunay
"""
from kafka import KafkaConsumer
import sys
bootstrap_servers = ['localhost:9092']
topicName = 'clientsfinal'
consumer = KafkaConsumer (topicName, group_id = 'client4final',bootstrap_servers = bootstrap_servers,
auto_offset_reset = 'earliest')





import requests 

from keras.models import model_from_json
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline
from ann_visualizer.visualize import ann_viz;

import h5py
import json




URL_json = "https://elasticbeanstalk-eu-central-1-335189602832.s3.eu-central-1.amazonaws.com/model/model2.json"

URL_h5 = "https://elasticbeanstalk-eu-central-1-335189602832.s3.eu-central-1.amazonaws.com/model/updated2.h5"

URL_send = 'http://localhost:5000/api/federated/models/send/client4'


def getGlobalModel(get_url):
    r = requests.get(url = get_url )
    f = open('C:\\Users\\MBICER14\\Desktop\\demo\\model2.json', 'wb')
    f.write(r.content)
    f.close()


def getUpdatedWeights(get_url):
    r = requests.get(url = get_url )
    f = open('C:\\Users\\MBICER14\\Desktop\\demo\\updated_weights2.h5', 'wb')
    f.write(r.content)
    f.close()
    
    
def sendWeights(get_url):
    files = {'file': open('third_client_model_weights.h5', 'rb')}
    requests.post(get_url, files=files)
    
    
    
    
    



seed =7
np.random.seed(seed)
dataframe=pd.read_csv("boston1.csv",delimiter =";")
array=dataframe.values


x1=array[0:100,0:13]
y1=array[0:100,13]

x2=array[100:180,0:13]
y2=array[100:180,13]

x3=array[180:,0:13]
y3=array[180:,13]


x = [x1, x2, x3]
y = [y1, y2, y3]


checkFirstTrain = True
countForDataSet = 0;
countForLoop = 0;










try:
    for message in consumer:
        print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,message.value))
        if (str(message.value, 'utf-8') == 'start2'):
            print('got it')
                
            if (checkFirstTrain):
              countForLoop +=1
              checkFirstTrain = False
              print("----------------------------------------------------------------------")
              print("Model getting from the server..")
              getGlobalModel(URL_json)
              print("Model obtained!")
              print("----------------------------------------------------------------------")
              print("Training starting...")
        
              # load json and create model
              json_file = open('model2.json', 'r')
              second_client = json_file.read()
              json_file.close()
              second_model = model_from_json(second_client)
        
        
              second_model.compile(loss='mean_squared_error', optimizer='adam')
              
              
              
              estimators = []
              estimators.append(('mlp', KerasRegressor(build_fn=second_model, epochs=100, batch_size=1, verbose=1)))
              pipeline = Pipeline(estimators)
                    
                
                    
              # evaluating model using the kfold method
              kfold = KFold(n_splits=10, random_state=seed)
              results = cross_val_score(pipeline,x[countForDataSet],y[countForDataSet], cv=kfold)
              print("Results: %.4f (%.4f) MSE" % (results.mean(), results.std()))
                
              print("FITTING THE MODEL NOW")
              # fitting the model
              second_model.fit(x[countForDataSet],y[countForDataSet],batch_size = 5 , epochs = 100)
            
              #scores=second_model.evaluate(x[countForDataSet],y[countForDataSet])
                
              #print("%s:%.2f%%"%(second_model.metrics_names[0],scores[1]*100))

              countForDataSet +=1
              countForDataSet = min(2,countForDataSet)
              #scores=second_model.evaluate(x[countForDataSet],y[countForDataSet])
        
              print("----------------------------------------------------------------------")
        
              second_model.save_weights("fourth_client_model_weights.h5")
              print("Saved fourth_client_model_weights to disk")
              print("----------------------------------------------------------------------")
              print("Weights sending the server..")
              sendWeights(URL_send)
              print("Updated sended!")
            else:
              print("ROUND : " + str(countForLoop))
              print("----------------------------------------------------------------------")   
              print("Updated weights getting from the server..")
              getUpdatedWeights(URL_h5)
              print("Updated weights obtained!")
              print("----------------------------------------------------------------------")
              # load json and create model
              json_file = open('model2.json', 'r')
              second_client = json_file.read()
              json_file.close()
              second_model = model_from_json(second_client)
              second_model.load_weights('updated_weights2.h5')
              second_model.compile(loss='mean_squared_error', optimizer='adam')
              
              
              
              estimators = []
              estimators.append(('mlp', KerasRegressor(build_fn=second_model, epochs=100, batch_size=1, verbose=1)))
              pipeline = Pipeline(estimators)
                    
                
                    
              # evaluating model using the kfold method
              kfold = KFold(n_splits=10, random_state=seed)
              results = cross_val_score(pipeline,x[countForDataSet],y[countForDataSet], cv=kfold)
              print("Results: %.4f (%.4f) MSE" % (results.mean(), results.std()))
                
              print("FITTING THE MODEL NOW")
              # fitting the model
              second_model.fit(x[countForDataSet],y[countForDataSet],batch_size = 5 , epochs = 100)
            
              #scores=second_model.evaluate(x[countForDataSet],y[countForDataSet])
                
              #print("%s:%.2f%%"%(second_model.metrics_names[0],scores[1]*100))
              
              
              
              
              
              if countForLoop<3:
                 countForLoop +=1
                 countForDataSet +=1
                 countForDataSet = min(2,countForDataSet)
                 print("----------------------------------------------------------------------")
                 second_model.save_weights("fourth_client_model_weights.h5")
                 print("Saved fourth_client_model_weights to disk")    
                 print("Weights sending the server..")
                 sendWeights(URL_send)
                 print("Updated sended!")
                  
except KeyboardInterrupt:
    sys.exit() 