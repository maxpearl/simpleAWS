"""
Simple_aws

SQS Functions

version .1
"""
import boto3
from aws_globals import *

class SqsSimple(object):
    def __init__(self, **kwargs):
        """
        Initializes SQS connection and Queue
        """
        if 'region_name' in kwargs:
            region_name = kwargs['region_name']
        else: 
            region_name = aws_default_region
        if 'profile' in kwargs:
            profile = kwargs['profile']
        else:
            profile = aws_default_profile

        session = boto3.session.Session(profile_name=kwargs['profile'],
                                    region_name=kwargs['region'])     
        self.sqs = session.resource('sqs')
        if 'queue' not in kwargs:
            queue_name = sqs_default_queue
        else:
            queue_name = kwargs['queue']
        
        self.queue = self.sqs.get_queue_by_name(QueueName=queue_name)

        return

    def get_sqs_messages(self):
        """
        Get all tenant messages waiting in SQS Queue
        """
        messages = self.queue.receive_messages()
        all_messages = []
        for message in messages:
            all_messages.append(message.body)
        
        return(all_messages)

    def send_sqs_message(self, **kwargs):
        """
        This will send an SQS message to the proper queue
        """
        if 'message' not in kwargs:
            print("No message!")
            return False

        self.queue.send_message(
            MessageBody=kwargs['message']
        )
            
        return True

    def create_queue(self):
        """
        Create new SQS Queue
        """
        new_queue = self.sqs.create_queue(QueueName=self.queue_name)

        return
        
    def purge_queue(self):
        """
        Purge a specific queue
        """
        
        self.queue.purge()
        
        return True