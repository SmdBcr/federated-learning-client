
from kafka import KafkaConsumer
import sys
bootstrap_servers = ['localhost:9092']
topicName = 'clientsfinal'
consumer = KafkaConsumer (topicName, group_id = 'client1final',bootstrap_servers = bootstrap_servers,
auto_offset_reset = 'earliest')



import requests 

from keras.models import model_from_json
import pandas as pd
import numpy as np


URL_json = "https://elasticbeanstalk-eu-central-1-335189602832.s3.eu-central-1.amazonaws.com/model/model.json"

URL_h5 = "https://elasticbeanstalk-eu-central-1-335189602832.s3.eu-central-1.amazonaws.com/model/updated.h5"

URL_send = 'http://localhost:5000/api/federated/models/send/client1'


def getGlobalModel(get_url):
    r = requests.get(url = get_url )
    f = open('C:\\Users\\MBICER14\\Desktop\\demo\\model.json', 'wb')
    f.write(r.content)
    f.close()


def getUpdatedWeights(get_url):
    r = requests.get(url = get_url )
    f = open('C:\\Users\\MBICER14\\Desktop\\demo\\updated_weights.h5', 'wb')
    f.write(r.content)
    f.close()
    
    
def sendWeights(get_url):
    files = {'file': open('first_client_model_weights.h5', 'rb')}
    requests.post(get_url, files=files)


seed =7
np.random.seed(seed)
dataframe=pd.read_csv("BBCN1.csv",delimiter =";")
array=dataframe.values


x1=array[0:100,0:11]
y1=array[0:100,11]

x2=array[100:180,0:11]
y2=array[100:180,11]

x3=array[180:,0:11]
y3=array[180:,11]


x = [x1, x2, x3]
y = [y1, y2, y3]


checkFirstTrain = True
countForDataSet = 0;
countForLoop = 0;





try:
    for message in consumer:
        print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,message.value))
        if (str(message.value, 'utf-8') == 'start1'):
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
                  json_file = open('model.json', 'r')
                  first_client = json_file.read()
                  json_file.close()
                  first_model = model_from_json(first_client)
            
            
                  first_model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
            
                  first_model.fit(x[countForDataSet],y[countForDataSet],epochs=375,batch_size=10)   
                  countForDataSet +=1
                  countForDataSet = min(2,countForDataSet)
            
                  scores=first_model.evaluate(x[countForDataSet],y[countForDataSet])
            
                  print("%s:%.2f%%"%(first_model.metrics_names[1],scores[1]*100))
            
                  print("----------------------------------------------------------------------")
                  first_model.save_weights("first_client_model_weights.h5")
                  print("Saved first_client_model_weights to disk")    
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
                  json_file = open('model.json', 'r')
                  first_client = json_file.read()
                  json_file.close()
                  first_model = model_from_json(first_client)
                  first_model.load_weights('updated_weights.h5')   
                  first_model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy']) 
                  first_model.fit(x[countForDataSet],y[countForDataSet],epochs=375,batch_size=10)
                  scores=first_model.evaluate(x[countForDataSet],y[countForDataSet])
                  print("%s:%.2f%%"%(first_model.metrics_names[1],scores[1]*100))
                  
                  if countForLoop<3:
                      countForLoop +=1
            
                      countForDataSet +=1
                      countForDataSet = min(2,countForDataSet)
                      print("----------------------------------------------------------------------")
                      first_model.save_weights("first_client_model_weights.h5")
                      print("Saved first_client_model_weights to disk")    
                      print("Weights sending the server..")
                      sendWeights(URL_send)
                      print("Updated sended!")
                  
                  
                  
                  
                  
                  
except KeyboardInterrupt:
    sys.exit()                 