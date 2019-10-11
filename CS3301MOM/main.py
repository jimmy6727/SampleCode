## main.py
## CS3301 - Component Technologies
## University of St. Andrews 
## Assignment: Practical 2 - Message Oriented Middleware

import pika
import consumer
import producer
import subprocess
from subprocess import check_output, PIPE
import sys
import os

active_agents = []

# Start consumer at 500 messages/second
def OpenConsumer():
    return subprocess.Popen("python3 consumer.py {}", shell=True, stdout = None)

def OpenProducer():
    return subprocess.Popen("python3 producer.py {}", shell=True, stdout=None)

def KillRandomQueue():
    to_kill = os.environ['random_queue']
    channel.queue_delete(to_kill)
#    os.environ['queueKill'] = "True"
#    return subprocess.Popen("python3 consumer.py {}", shell=True, stdout=None)


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

OpenConsumer()
OpenProducer()
#KillRandomQueue()
