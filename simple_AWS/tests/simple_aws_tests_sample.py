import os
import time
import json
import csv
import sys
sys.path.insert(0, '..')
from dynamodb_functions import *
from s3_functions import *
from sns_functions import *
from sqs_functions import *
from ec2_functions import *
from aws_functions import *

def dynodb_tests():
    # DynamoDB Tests

    test_table = "test_table"
    test_new_table = "test_new_table"
    test_region = "us-west-1"
    test_profile = "default"

    dbsimple = DynamodbSimple(table_name=test_table, region_name=test_region, profile=test_profile)

    exists = dbsimple.check_table()
    if exists:
        print("Test Table exists!")
    else:
        print("Test table does not exist!")

    
    # Creating table
    print("Table creating...")
    dbsimple = DynamodbSimple(table_name=test_new_table, region_name=test_region, profile=test_profile)
    dbsimple.create_table(
        partition_key='fee',
        sort_key='fie',
        throughput='5'
    )
    
    # list tables
    dbsimple = DynamodbSimple(region_name=test_region, profile=test_profile)
    table_list = dbsimple.list_tables()
    print(f"Table list: {table_list}")

    
    # Delete table
    dbsimple = DynamodbSimple(table_name=test_new_table, region_name=test_region, profile=test_profile)
    dbsimple.delete_table()
    print("Deleting table...")

    # wait 2 minutes
    time.sleep(120)
    

    # List again
    dbsimple = DynamodbSimple(region_name=test_region, profile=test_profile)
    table_list = dbsimple.list_tables()
    print(f"New table list: {table_list}")
    

    # Grab test data, create list of dicts
    data = []
    with open('test.csv', 'r') as lf:
        reader = csv.DictReader(lf)
        for row in reader:
            new_row = {}
            for key in row.keys():
                new_row[key] = row[key]
            if new_row:
                data.append(new_row)

    
    # Write Data in Bulk
    print("Writing data...")
    dbsimple = DynamodbSimple(table_name=test_table, region_name=test_region, profile=test_profile)
    dbsimple.batch_write_items(items=data)
    

    # Write individual items
    dbsimple = DynamodbSimple(table_name=test_table, region_name=test_region, profile=test_profile)
    items = [
        {'ID': '999999', 'first_name': 'FOOBY', 'last_name': 'Furby'},
        {'ID': '888888', 'first_name': 'GOOBY', 'last_name': 'Gurby'}
    ]

    print("Writing items...")
    for item in items:
        dbsimple.insert_item(item=item)

    # Dynamo Query
    dbsimple = DynamodbSimple(table_name=test_table, region_name=test_region, profile=test_profile)
    data = dbsimple.dynamo_query(
        field='ID',
        value='999999'
    )
    print(f"Result of query: {data}")

    # Dynamo Scan
    dbsimple = DynamodbSimple(table_name=test_table, region_name=test_region, profile=test_profile)
    data = dbsimple.dynamo_scan(
        key='first_name',
        value='GOOBY'
    )
    print(f"Resut of scan: {data}")

    # Get all data
    dbsimple = DynamodbSimple(table_name=test_table, region_name=test_region, profile=test_profile)
    all_data = dbsimple.get_all()
    print(f"Returned {len(all_data)} rows.")

    # Delete a row
    dbsimple = DynamodbSimple(table_name=test_table, region_name=test_region, profile=test_profile)
    print("Deleting Item...")
    dbsimple.delete_item(
        key='ID',
        value='888888'
    )
    all_data = dbsimple.get_all()
    print(f"Returned {len(all_data)} rows.")

    # Change an entry
    dbsimple = DynamodbSimple(table_name=test_table, region_name=test_region, profile=test_profile)
    print("Updating item...")
    dbsimple.update_item(
        key='first_name',
        value='Fiiby',
        id_key='ID',
        id_value='999999'
    )
    new_value = dbsimple.dynamo_query(
        field='ID',
        value='999999'
    )
    print(f"New value: {new_value}")


    return

def s3_tests():
    # s3 tests

    test_bucket = "simple-aws-test"
    test_new_bucket = "simple-aws-new-test"
    test_region = "us-west-1"
    test_profile = "default"
    test_text = """
    Hundreds of thousands light years shores of the cosmic ocean circumnavigated white dwarf Rig Veda. 
    Courage of our questions something incredible is waiting to be known extraordinary claims require 
    extraordinary evidence brain is the seed of intelligence laws of physics extraordinary claims require 
    extraordinary evidence. Dream of the mind's eye invent the universe emerged into consciousness made 
    in the interiors of collapsing stars something incredible is waiting to be known finite but unbounded.
    """
    test_local_file = '/tmp/aliens.jpg'
    test_file_name = 'aliens.jpg'

   # List Buckets
    if (function == 'list') or (function == 'all'):
        s3simple = S3Simple(region_name=test_region, profile=test_profile)
        bucket_list = s3simple.list_buckets()
        print(f"Buckets: {bucket_list}")

    # Bucket Contents
    if (function == 'contents') or (function == 'all'):
        s3simple = S3Simple(bucket_name=test_bucket, region_name=test_region, profile=test_profile)
        file_list = s3simple.s3_bucket_contents()

        print(f"Contents of test bucket: {file_list}")

    # Filtered List
    if (function == 'filtered') or (function == 'all'):
        s3simple = S3Simple(bucket_name=test_bucket, region_name=test_region, profile=test_profile)
        filtered_list = s3simple.s3_bucket_filter(prefix='Decorating the Sky.jpg')

        print(f"Filtered contents of test bucket: {filtered_list}")

    # Download a file
    if (function == 'download') or (function == 'all'):
        s3simple = S3Simple(bucket_name=test_bucket, region_name=test_region, profile=test_profile)
        s3simple.download_file(file_name='Decorating the Sky.jpg', output_file='/tmp/Decorating the Sky.jpg')

        if os.path.exists('/tmp/Decorating the Sky.jpg'):
            print("File Downloaded Properly!")
        else:
            print("File not downloaded!")
    
    # create a bucket
    if (function == 'new') or (function == 'all'):
        s3simple = S3Simple(bucket_name=test_new_bucket, region_name=test_region, profile=test_profile)
        if not s3simple:
            print("Problem with profile!!")
            return

        new_bucket = s3simple.s3_new_bucket()

        print(f"New Bucket: {new_bucket}")
        new_bucket_list = s3simple.list_buckets()
        print(f"New Bucket List: {new_bucket_list}")

    # delete a bucket
    if (function == 'remove') or (function == 'all'):
        s3simple = S3Simple(bucket_name=test_new_bucket, region_name=test_region, profile=test_profile)
        s3simple.s3_delete_bucket()

        new_bucket_list = s3simple.list_buckets()
        print(f"New Bucket List: {new_bucket_list}")

    # Send text to bucket
    if (function == 'text') or (function == 'all'):
        print("Sending text to S3...")
        s3simple = S3Simple(bucket_name=test_bucket, region_name=test_region, profile=test_profile)
        key = 'test_item.txt'
        s3simple.put_to_s3(key=key, body=test_text)

    # Send file to S3
    if (function == 'file') or (function == 'all'):
        print("Sending file to S3...")
        s3simple = S3Simple(bucket_name=test_bucket, region_name=test_region, profile=test_profile)
        s3simple.send_file_to_s3(local_file=test_local_file, s3_file=test_file_name, public=True)

    # Delete file
    if (function == 'delete') or (function == 'all'):
        # First send file
        print("Sending text for file for deletion...")
        s3simple = S3Simple(bucket_name=test_bucket, region_name=test_region, profile=test_profile)
        d_key = 'test_item_to_delete.txt'
        s3simple.put_to_s3(key=key, body=test_text)

        # then delete it
        print("Deleting file")
        s3simple = S3Simple(bucket_name=test_bucket, region_name=test_region, profile=test_profile)
        s3simple.delete_s3_file(file_name=d_key)

    return

def sqs_tests():
    # SQS tests

    test_region = "us-east-1"
    test_profile = "default"
    test_queue = "test-queue"
    test_new_queue = "test-new-queue"
    test_message = "This is a test of the emergency SQS system!"
    test_second_message = "Really, another test, OK?"

    # Does a queue exist?
    sqssimple = sqsSimple(region_name=test_region, profile=test_profile, queue=test_queue)
    exists = sqssimple.queue_exists()
    
    if exists:
        print("Test Queue exists!")
    else:
        print("Test Queue does not exist!")

    # list queues
    sqssimple = sqsSimple(region_name=test_region, profile=test_profile)
    queues = sqssimple.list_queues()

    print(f"Queues: {queues}")

    # Create a new queue
    print("Creating new queue...")
    sqssimple = sqsSimple(region_name=test_region, profile=test_profile, queue=test_new_queue)
    sqssimple.create_queue()

    # wait
    time.sleep(120)

    # list queues again
    sqssimple = sqsSimple(region_name=test_region, profile=test_profile)
    queues = sqssimple.list_queues()

    print(f"Queues: {queues}")

    
    # Delete a queue
    sqssimple = sqsSimple(region_name=test_region, profile=test_profile, queue=test_new_queue)
    sqssimple.delete_queue()

    # wait
    time.sleep(120)

    # list queues again
    sqssimple = sqsSimple(region_name=test_region, profile=test_profile)
    queues = sqssimple.list_queues()

    print(f"Queues: {queues}")

    # Send a message
    print("Sending messages...")
    sqssimple = sqsSimple(region_name=test_region, profile=test_profile, queue=test_queue)
    sqssimple.send_sqs_message(message=test_message)
    sqssimple.send_sqs_message(message=test_second_message)

    # Read messages
    sqssimple = sqsSimple(region_name=test_region, profile=test_profile, queue=test_queue)
    messages = sqssimple.get_sqs_messages(num_messages=5)
    print(f"Here are the messages: {messages}")

    # Purge Queue
    print("Purging Queue...")
    sqssimple = sqsSimple(region_name=test_region, profile=test_profile, queue=test_queue)
    sqssimple.purge_queue()

    # wait
    time.sleep(120)

    # List messages again
    sqssimple = sqsSimple(region_name=test_region, profile=test_profile, queue=test_queue)
    messages = sqssimple.get_sqs_messages(num_messages=5)
    print(f"Here are the messages: {messages}")

    return
    
def sns_tests():
    # SNS test

    test_region = "us-east-1"
    test_profile = "default"
    test_arn = "arn:aws:sns:us-east-1:650307174203:test-topic"
    test_subject = "Testing Simple AWS"
    test_message = "You go, girl!"

    # List Topics
    snssimple = snsSimple(region_name=test_region, profile=test_profile)
    topics = snssimple.list_topics()

    print(f"Topics: {topics}")

    # List Subscriptions
    snssimple = snsSimple(region_name=test_region, profile=test_profile)
    subs = snssimple.list_subscriptions()

    print(f"Subscriptions: {subs}")

    # Sending message
    print("Sending message... check your inbox.")
    snssimple = snsSimple(region_name=test_region, profile=test_profile)
    result = snssimple.send_notification(arn=test_arn, subject=test_subject, message=test_message)

    return

def inventory():
    test_region = "us-east-1"
    test_profile = "default"
    
    service_list = [
        'ec2',
        'dynamodb',
        's3',
        'sns',
        'sqs'
    ]

    aws = awsSimple(region_name=test_region, profile=test_profile)
    # Regions
    for service in service_list:
        print(f"Service: {service}")
        regions = aws.list_regions(service=service)
        for region in regions:
            if service == 'ec2':
                ec2 = ec2Simple(profile=test_profile, region_name=region)
                ec2.list_instances()
    return

    
if __name__ == '__main__':
    while True:
        service = input("Which service to test (dyn, s3, sqs, sns, inv, Quit)?")
        if service == 'dyn':
            dynodb_tests()
        elif service == 's3':
            func = input("Which function to test (list, contents, filtered, download, new, remove, text, file, delete, all)?")
            s3_tests(func)
        elif service == 'sqs':
            sqs_tests()
        elif service == 'sns':
            sns_tests()
        elif service == 'inv': # inventory
            inventory()
        else:
            exit()
            