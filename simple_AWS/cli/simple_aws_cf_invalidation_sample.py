"""
Creates invalidation for a cloudfront distribution based on alias
"""
from simple_AWS.aws_functions import *
from simple_AWS.cloudfront_functions import *
import click

@click.command()
@click.option('--region', type=str, help="AWS Region", default='us-east')
@click.option('--profile', type=str, help="AWS Auth Profile", default='default')
@click.option('--domain', type=str, help="Domain for invalidation", required=True)
@click.option('--path', type=str, help="Path to invalidate", default='/*')
@click.option('--dryrun', is_flag=True, default=False, help="Dry run - will just return info on distribution")

def invalidate(region, profile, domain, path, dryrun):
    """
    Will create invalidation of a path depending on domain
    """
    # First, get all distributions
    cfsimple = Cloudfront_Simple(region_name=region, profile=profile)
    dists = cfsimple.cf_list()
    
    for dist in dists: # get the one we want
        for alias in dist['Aliases']['Items']:
            if alias == domain:
                cf_id = dist['Id']
                dist_info = dist
                print(f"Dist ID: {cf_id}, domain: {dist['DomainName']}")

    # Create invalidation
    if dryrun:
        print(f"Dry Run! Distribution info: {dist_info}")
    else:
        response = cfsimple.cf_invalidate(cf_id, path)
        print(f"Response to invalidation: {response}")

    return

if __name__ == '__main__':
  invalidate()

            