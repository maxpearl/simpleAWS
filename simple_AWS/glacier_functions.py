"""
Simple_aws Glacier Functions

"""
import boto3
import io

class GlacierSimple(object):

    def __init__(self, **kwargs):
        """
        Initializes Glacier connection
        """
        if 'region_name' in kwargs:
            self.region_name = kwargs['region_name']

        if 'profile' in kwargs:
            profile = kwargs['profile']

        self.session = boto3.session.Session(profile_name=profile,
                                    region_name=self.region_name)
        self.glacier = self.session.resource('glacier')

        return

    def list_vaults(self):
        """
        Returns a list of all vaults
        """
        vaults_iterator = self.glacier.vaults.all()

        vault_names = []
        for vault in vaults_iterator:
            vault_names.append(vault.name)

        return (vault_names)

