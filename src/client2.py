from kafka import KafkaConsumer
from kafka import KafkaProducer
from json import loads, dumps

# from keras import Sequential
# from keras.layers import Dense

if __name__ == '__main__':
    consumer = KafkaConsumer(
        'test',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group9',
       )

    for message in consumer:
        message = message.value
        print("MSG Received: ", message)

    # model = Sequential()
    # model.add(Dense(35, input_dim=100, activation="relu", kernel_initializer="normal"))
    # model.add(Dense(16, activation="relu", kernel_initializer="normal"))
    # model.add(Dense(1, kernel_initializer="normal"))
    # model.compile(loss='mean_squared_error', optimizer='adam')
    #
    # modelToSend = model.to_json()

    # producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
    #                          acks=1,api_version=(0, 10, 1),
    #                          compression_type=None)
    #
    # print(producer)
    # producer.send('test', key=b'client-x', value=b'model=json')
    # print("MSG sent")
    #
    # producer.close()

