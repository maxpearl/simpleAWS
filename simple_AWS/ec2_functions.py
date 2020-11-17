"""
EC2 Functions
"""
import boto3

class ec2Simple(object):

    def __init__(self, **kwargs):
        """
        Initializes EC2 connection
        """
        if 'region_name' in kwargs:
            region_name = kwargs['region_name']

        if 'profile' in kwargs:
            profile = kwargs['profile']

        session = boto3.session.Session(profile_name=profile,
                                    region_name=region_name)
        self.ec2 = session.resource('ec2')

        return

    def list_instances(self):
        instance_iterator = self.ec2.instances.all()
        for instance in instance_iterator:
            print(instance)

        return
