import pika
from datetime import datetime
import time
import sys
import random
import os
import pdb

class Consumer:
    
    def __init__(self, channel):
        print("Consumer constructor called")
        
    def StartConsuming(self, rate, channel, auto_reorder = True, auto_duplicate_drop = True):
        print("Consumer Start method called")
        types_of_messages = ['DtoC',
                             'DtoS',
                             'CtoD',
                             'CtoS',
                             'Payments']
        
        # Connect to server unless we're already connected
        if not hasattr(Consumer, 'channel'):
            self.channel = channel
        
        # Declare topic type exchange named mExchange
        self.channel.exchange_declare(exchange='mExchange',
                                 exchange_type='topic')
        
        #Empty list to store queue names
        self.queues = [] #Empty list to store queue names
        
        j=0
        for j in range(len(types_of_messages)):
    
            msg_type = types_of_messages[j]
            
            # Create exclusive queue with random name for each different topic of message
            result = self.channel.queue_declare('',exclusive=True)
            
            # Store name of queue for testing purposes
            queue_name = result.method.queue
            self.queues.append(queue_name)
            
            # Bind random queue to exchange
            self.channel.queue_bind(exchange='mExchange',
                               queue=queue_name,
                               routing_key=msg_type)
        
        # Save name of randomly selected queue to environment
        os.environ['random_queue'] = str(random.choice(self.queues))
        
        # Messages consumed per second
        CONSUME_RATE = rate 
        
        now = datetime.now()
        self.auto_reorder = auto_reorder
        self.auto_duplicate_drop = auto_duplicate_drop
        messages_master_c = []
        potential_dropped_messages = []
        
        # Callback function
        def callback(ch, method, properties, body):
            global now
            now = datetime.now()
            
            print(" [x] Received %r" % body)
            
            # Dealing with out of order messages, missed messages, and duplicated messages
            
            # Simulated expected-order of message
            str_m = body.decode('utf-8')
            mo = str_m[-3:]
            
            if int(mo) == 0:
                messages_master_c.append(0)
            
            last_processed = max(messages_master_c)
            diff = int(mo)-int(last_processed)
            
#            if int(mo) == 502:
#                pdb.set_trace() #use for debugging
            
            
            # If diff = 0 or we've already processed the message, then we are dealing with a duplicate message
            if diff == 0 or int(mo) in messages_master_c: 
                print("This message is a duplicate of another message.")
                if self.auto_duplicate_drop == False:
                    a = input('Would you like to drop this duplicated message? (Y/N) ')
                    if (str(a) == 'Y'):
                        print("Dropping duplicated message")
                if self.auto_duplicate_drop == True:
                    print("Dropped duplicate message at index " + mo)
                    
            # If diff > 1 then we missed a message in our expected ordering and need to find the ones we missed
            elif diff > 1 and not int(mo) in potential_dropped_messages:
                print("Possible missed message at or before index " + mo + " we will look for this message for you.")
                to_find_l = max(messages_master_c)
                for x in range(to_find_l, int(mo)):
                    potential_dropped_messages.append(x)
                
            # We are dealing with messages received out of the expected order
            elif diff > 1 and int(mo) in potential_dropped_messages: 
                print("Expected message "+str_m+" at index " + mo)
                if self.auto_reorder == False:
                    a = input('Would you like to move this message to its expected index? (Y/N) ')
                    if (str(a) == 'Y'):
                        print("Moving message to its expected index")
                if self.auto_reorder == True:
                    print("Moving message to its expected index")
            
            # If diff == 1 then everything went as expected
            elif diff == 1:    
                print("Message order confirmed")
                if mo != 0:
                    messages_master_c.append(int(mo))
            
            #Simulate time 
            elapsed = (datetime.now()-now).total_seconds()
            wait_time = 1/CONSUME_RATE-elapsed
            if wait_time > 0:
                time.sleep(wait_time)
            now = datetime.now()
            
            
        # Specify queue this particular callback function should receive messages from (iterate through all queues)
        for j in range(len(self.queues)):
            q = self.queues[j]
            self.channel.basic_consume(queue=q,
                                       auto_ack = True,
                                       on_message_callback=callback)
        
        #Start infinite loop searching for messages
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

        
# We don't want main to run on import
def main():   
    pass 

# We only want main to run when called
if __name__ == "__main__":
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    
    Cons = Consumer(channel = channel)
    Cons.StartConsuming(rate=500, channel = channel, auto_reorder = True, auto_duplicate_drop = True)
    
main()