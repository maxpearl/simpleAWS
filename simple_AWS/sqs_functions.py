"""
Simple_aws

SQS Functions

"""
import boto3

class sqsSimple(object):
    def __init__(self, **kwargs):
        """
        Initializes SQS connection and Queue
        """
        if 'region_name' in kwargs:
            region_name = kwargs['region_name']

        if 'profile' in kwargs:
            profile = kwargs['profile']

        session = boto3.session.Session(profile_name=profile,
                                    region_name=region_name)     
        self.sqs = session.resource('sqs')

        if 'queue' in kwargs:
            self.queue_name = kwargs['queue']

        return

    def queue_exists(self):
        """
        Does the queue exist?
        """
        if hasattr(self,'queue_name'):
            try:
                queue = self.sqs.get_queue_by_name(QueueName=self.queue_name)
            except:
                return False
        else:
            return False

        return queue

    def list_queues(self):
        """
        List queues
        """
        queues = []
        queue_iterator = self.sqs.queues.all()
        for queue in queue_iterator:
            queues.append(queue.url)

        return queues

    def get_sqs_messages(self, **kwargs):
        """
        Get all tenant messages waiting in SQS Queue
        """
        queue = self.sqs.get_queue_by_name(QueueName=self.queue_name)
        if 'num_messages' in kwargs:
            num_messages = kwargs['num_messages']
        else:
            num_messages = 100
            
        messages = queue.receive_messages(MaxNumberOfMessages=num_messages)
        all_messages = []
        for message in messages:
            all_messages.append(message.body)
        
        return(all_messages)

    def send_sqs_message(self, **kwargs):
        """
        This will send an SQS message to the proper queue
        """

        if 'message' not in kwargs:
            return False

        queue = self.sqs.get_queue_by_name(QueueName=self.queue_name)
        queue.send_message(
            MessageBody=kwargs['message']
        )
            
        return

    def create_queue(self):
        """
        Create new SQS Queue
        """
        new_queue = self.sqs.create_queue(QueueName=self.queue_name)
        print(new_queue)

        return
        
    def purge_queue(self):
        """
        Purge a specific queue
        """
        queue = self.sqs.get_queue_by_name(QueueName=self.queue_name)
        queue.purge()
        
        return

    def delete_queue(self):
        """
        Delete a specific queue
        """
        queue = self.sqs.get_queue_by_name(QueueName=self.queue_name)
        queue.delete()

        return