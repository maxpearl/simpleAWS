import sys
sys.path.insert(0, '..')
from dynamodb_functions import *
from s3_functions import *
from sns_functions import *
from sqs_functions import *
from ec2_functions import *
from aws_functions import *
from cloudfront_functions import *

def inventory(service):
    test_region = "us-east-1"
    test_profile = "default"

    aws = awsSimple(region_name=test_region, profile=test_profile)
    print(f"Services Inventoried: {service}")
    if service == 'ec2' or service == 'all':
        this_service = 'ec2'
        print(f"EC2:")
        regions = aws.list_regions(service=this_service)
        for region in regions:
            print(f"Region: {region}")
            try:
                ec2 = ec2Simple(region_name=region, profile=test_profile)
                instances = ec2.list_instances()
                for instance in instances:
                    print(f"Instance: {instance}")
            except:
                print("Region not available for EC2")
    if service == 'dynamodb' or service == 'all':
        this_service = 'dynamodb'
        print("DynamoDB")
        regions = aws.list_regions(service=this_service)
        for region in regions:
            print(f"Region: {region}")
            try:
                dynamodb = DynamodbSimple(region_name=region, profile=test_profile)
                tables = dynamodb.list_tables()
                print(f"Tables: {tables}")
            except:
                print("Region not available for DynamoDB")
    if service == 's3' or service == 'all':
        print("S3")
        s3simple = S3Simple(profile=test_profile, region_name='us-east-1') # S3 is global
        bucket_list = s3simple.list_buckets()
        print(f"Buckets: {bucket_list}")
    if service == 'sqs' or service == 'all':
        print("SQS")
        this_service = 'sqs'
        regions = aws.list_regions(service=this_service)
        for region in regions:
            print(f"Region: {region}")
            try:
                sqs_simple = sqsSimple(region_name=region, profile=test_profile)
                sqs_list = sqs_simple.list_queues()
                print(f"SQS Queues: {sqs_list}")
            except:
                print("Region not available for SQS")
    if service == 'sns' or service == 'all':
        print("SNS")
        this_service = 'sns'
        regions = aws.list_regions(service=this_service)
        for region in regions:
            print(f"Region: {region}")
            try:
                sns_simple = snsSimple(region_name=region, profile=test_profile)
                topics = sns_simple.list_topics()
                print(f"Topics: {topics}")
                sns_simple = snsSimple(region_name=region, profile=test_profile)
                subscriptions = sns_simple.list_subscriptions()
                print(f"Subscriptions: {subscriptions}")
            except:
                print("Region not available for SNS")
    if service == 'cf' or service == 'all':
        print("CloudFront is global")
        cfsimple = Cloudfront_Simple(region_name=test_region, profile=test_profile)
        dists = cfsimple.cf_list()

        print(f"List of distributions in {test_region} for profile {test_profile}")
        for dist in dists:
            print(f"URL: {dist['DomainName']}")
            for alias in dist['Aliases']['Items']:
                print(f"Alias: {alias}")

    return

    
if __name__ == '__main__':
    while True:
        service = input("Which service to inventory (ec2, dyn, s3, sqs, sns, cf, all, (q)uit)?")
        if service.lower() == 'q':
            exit()
        else:
            inventory(service)

            