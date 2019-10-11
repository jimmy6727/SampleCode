import pika
import time
from datetime import datetime

class Producer:
    
    def __init__(self):
        print("Producer constructor called")
        
    def StartPublishing(self, rate, InjectErrorTest = False):
        print("Producer Publish method called")
        
        types_of_messages = ['DtoC',
                             'DtoS',
                             'CtoD',
                             'CtoS',
                             'Payments']
        
        # Connect to server unless we're already connected
        if not hasattr(Producer, 'channel'):
            
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            channel = connection.channel()
            self.channel = channel
        
        # Declare topic exchange to handle all messages (idempotent)
        channel.exchange_declare(exchange='mExchange', exchange_type='topic')
        
        MESSAGE_RATE = int(rate) # Rate of simulated message transfer per second of each type of message
        messages_master_p = []
        # Deliver messages of different types
        i=0
        j=0
        c=0
        # Time the loop to simulate messages per second
    #   while True:
        now = datetime.now()
        for j in range(len(types_of_messages)):
            msg_type = types_of_messages[j] # Each type of message will be sent MESSAGE_RATE times per second
            for i in range(int(MESSAGE_RATE/len(types_of_messages))):
                message = msg_type+"message"+str("{0:0=3d}".format(c))
                messages_master_p.append(message)
                channel.basic_publish(exchange='mExchange', 
                                      routing_key=msg_type, 
                                      body=message)
                i += MESSAGE_RATE/int(len(types_of_messages))
                print(" [x] Sent %r" % message)
                time_elapsed = (datetime.now() - now).total_seconds()
                wait = 1 - time_elapsed
                time.sleep(wait if wait > 0 else 0)
                c = c+1
                
        # Test dropped messages, duplicate messages, and out 
        # of order messages at message index 996 so we can see the output
        if InjectErrorTest == True:
        
            #Test duplicate messages
            channel.basic_publish(exchange='mExchange', 
                          routing_key=msg_type, 
                          body='Paymentsmessage497')
            print(" [x] Sent %r" % 'Paymentsmessage497')

            #Test dropped message
            channel.basic_publish(exchange='mExchange', 
                          routing_key=msg_type, 
                          body='Paymentsmessage502')
            print(" [x] Sent %r" % 'Paymentsmessage502')
            
            #Test out of order message
            channel.basic_publish(exchange='mExchange', 
                          routing_key=msg_type, 
                          body='Paymentsmessage501')
            print(" [x] Sent %r" % 'Paymentsmessage501')
            
            print("\n \n \n \n \n \n If you've made it this far, all tests were successful.")
    
# We don't want main to run on import
def main():   
    pass

## Main function starts publishing        
if __name__ == "__main__":   
    
    Prod = Producer()
    Prod.StartPublishing(rate=500, InjectErrorTest = True)
    
main()