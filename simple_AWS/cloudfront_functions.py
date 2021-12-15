"""
Cloudfront functions library

Super simplified AWS functions.
"""
import boto3

class Cloudfront_Simple(object):

    def __init__(self, **kwargs):
        """
        Initializes AWS connection
        """
        if 'region_name' in kwargs:
            self.region_name = kwargs['region_name']

        if 'profile' in kwargs:
            profile = kwargs['profile']

        self.session = boto3.session.Session(profile_name=profile,
                                    region_name=self.region_name)

        self.cf_client = self.session.client('cloudfront')

        return

    def cf_list(self):
        """
        Lists cloudfront distributions in one region
        :returns dict list?
        """

        distributions = []
        truncated = True
        marker = ''
        while truncated:
            distribution_list = self.cf_client.list_distributions(Marker=marker)
            distributions.extend(distribution_list['DistributionList']['Items'])
            if not distribution_list['DistributionList']['IsTruncated']:
                truncated = False
            else:
                marker = distribution_list['DistributionList']['NextMarker']

        return distributions