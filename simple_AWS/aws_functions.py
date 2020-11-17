"""
Overall AWS Functions
"""
import boto3

class awsSimple(object):

    def __init__(self, **kwargs):
        if 'region_name' in kwargs:
            region_name = kwargs['region_name']

        if 'profile' in kwargs:
            profile = kwargs['profile']

        self.session = boto3.session.Session(profile_name=profile,
                                        region_name=region_name)
        return

    def list_regions(self, **kwargs):
        regions = self.session.get_available_regions(kwargs['service'])

        return regions
