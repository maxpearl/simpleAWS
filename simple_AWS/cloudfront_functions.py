"""
Cloudfront functions library

Super simplified AWS functions.
"""
import time
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

    def cf_details(self, **kwargs):
        """
        Returns details based on ID, domain, alias or origin
        :param kwarg id
        :param kwarg domain
        :param kwarg alias
        :param kwarg origin
        :returns dict with details
        """

        if 'id' in kwargs and kwargs['id']:
            cf_id = kwargs['id']
            domain = False
            alias = False
            origin = False
        elif 'domain' in kwargs and kwargs['domain']:
            domain = kwargs['domain']
            cf_id = False
            alias = False
            origin = False
        elif 'alias' in kwargs and kwargs['alias']:
            alias = kwargs['alias']
            cf_id = False
            domain = False
            origin = False
        elif 'origin' in kwargs and kwargs['origin']:
            origin = kwargs['origin']
            domain = False
            alias = False
            cf_id = False
        else:
            return False

        # First, get distribution list

        details = []
        distributions = self.cf_list()
        for dist in distributions:
            if dist['Id'] == cf_id:
                return [dist]
            elif dist['DomainName'] == domain:
                return [dist]
            elif origin:
                for cf_origin in dist['Origins']['Items']:
                    if cf_origin['DomainName'] == origin:
                        details.append(dist)
            else: # assumption is alias is left
                for cf_alias in dist['Aliases']['Items']:
                    if cf_alias == alias:
                        details.append(dist)

        return details

    def cf_invalidate(self, cf_id, path):
        """
        Creates an invalidation on a Cloudfront distribution
        :param self
        :param cf_id - distribution id
        :param path - path to invalidate
        """
        now = str(time.time())

        response = self.cf_client.create_invalidation(
            DistributionId=cf_id,
            InvalidationBatch = {
                'Paths': {
                    'Quantity': 1,
                    'Items': [
                        path,
                    ]
                },
                'CallerReference': now
            }
        )     

        return response
    