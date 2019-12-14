"""
Simple_aws

SNS Functions 

version 0.1
"""
import boto3

class snsSimple(object):

    def __init__(self, **kwargs):
        """
        Initializes SNS connection
        """
        if 'region_name' in kwargs:
            region_name = kwargs['region_name']
        else: 
            region_name = aws_default_region
        if 'profile' in kwargs:
            profile = kwargs['profile']
        else:
            profile = aws_default_profile

        session = boto3.session.Session(profile_name=profile,
                                    region_name=region_name)
        self.sns = session.resource('sns')

        return

    def send_notification(self, **kwargs):
        """
        Function to send SNS notification when a new registry entry is made
        
        """
        if 'arn' not in kwargs:
            arn = sns_default_arn
        else:
            arn = kwargs['arn']
        if 'subject' not in kwargs:
            subject = sns_default_subject
        else:
            subject = kwargs['subject']
        
        if 'message' not in kwargs:
            message = sns_default_message
        else:
            message = kwargs['message']
        topic  = self.sns.Topic(arn)
        result = topic.publish(
                TopicArn=arn,
                Subject=subject,
                Message=message
            )
        return