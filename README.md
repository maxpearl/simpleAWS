[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0) ![pypi](https://img.shields.io/pypi/v/simple-AWS.svg) [![https://gitter.im/simple-AWS/community](https://badges.gitter.im/simple-AWS/community.svg)](https://gitter.im/simple-AWS/simple-AWS) ![issues](https://img.shields.io/github/issues/maxpearl/simpleAWS) ![last commit](https://img.shields.io/github/last-commit/maxpearl/simpleAWS)

# SimpleAWS

Version 0.1.6

Simplified Libraries for some of the most common AWS resources. The purpose of SimpleAWS is to add one layer of abstraction, and remove a lot of the guess-work from interfacing with some AWS resources.

The options are limited on purpose - this is *not* designed to replace boto3, but to provide an easier entry into using AWS resources with python.

## AWS Requirements

SimpleAWS uses profiles and secret/access keys. Put a file called 'credentials' inside the .aws directory in your home directory (the home of the user running this code.) The format of the file is:
```
[profilename]
aws_access_key_id = <key>
aws_secret_access_key = <key>
```

## Installation

`pip install simple-aws`

## Usage

```
from simple_AWS.aws_functions import *
from simple_AWS.dynamodb_functions import *
from simple_AWS.s3_functions import *
from simple_AWS.sns_functions import *
from simple_AWS.sqs_functions import *
```

### Overall

*Get Regions for a service*

`regions = aws.list_regions(service=service)`

### S3

*List buckets*

```
s3simple = S3Simple(region_name='region', profile='profile')
bucket_list = s3simple.list_buckets()
# returns a list
```

*Get a list of files in a bucket*
```
s3simple = S3Simple(region_name='region', profile='profile', bucket_name='bucket-name')
file_list = s3simple.s3_bucket_contents()
# returns a list
```

*Get a filtered list of files in a bucket*
```
s3simple = S3Simple(region_name='region', profile='profile', bucket_name='bucket-name')
filtered_list = s3simple.s3_bucket_filter(prefix='file_name.ext')
# returns a list
```

*Download a file*
```
s3simple = S3Simple(region_name='region', profile='profile', bucket_name='bucket-name')
s3simple.download_file(file_name='file_name.ext', output_file='/path/file_name.txt')
```

*Create Bucket*
```
s3simple = S3Simple(region_name='region', profile='profile', bucket_name='new-bucket-name')
new_bucket = s3simple3.s3_new_bucket()
```

*Delete Bucket*
``` 
s3simple = S3Simple(region_name='region', profile='profile', bucket_name='bucket-name')
s3simple.s3_delete_bucket()
```

*Saving text to file*
```
s3simple = S3Simple(region_name='region', profile='profile', bucket_name='bucket-name')
key = 'test_item.txt'
    body = """
    Hundreds of thousands light years shores of the cosmic ocean circumnavigated white dwarf Rig Veda. 
    Courage of our questions something incredible is waiting to be known extraordinary claims require 
    extraordinary evidence brain is the seed of intelligence laws of physics extraordinary claims require 
    extraordinary evidence. Dream of the mind's eye invent the universe emerged into consciousness made 
    in the interiors of collapsing stars something incredible is waiting to be known finite but unbounded.
    """
s3simple.put_to_s3(key=key, body=body)
```

*Sending file to S3*
```
s3simple = S3Simple(region_name='region', profile='profile', bucket_name='bucket-name')
s3simple.send_file_to_s3(local_file='/path/file_name.ext', s3_file='file_name.ext')
```

To make that file publically available (not recommended!):
```
s3simple = S3Simple(region_name='region', profile='profile', bucket_name='bucket-name')
s3simple.send_file_to_s3(local_file='/path/file_name.ext', s3_file='file_name.ext', public=True)
```

*Delete File*
```
s3simple = S3Simple(region_name='region', profile='profile', bucket_name='bucket-name')
s3simple.delete_s3_file(file_name=key)
```

### DynamoDB

*Checking to see if a table exists*
```
dbsimple = DynamodbSimple(table_name='table_name', region_name='region', profile='profile') 
# region and profile are optional
if dbsimple.check_table(): # returns True/False
    ...

```

*List all Tables*
```
dbsimple = DynamodbSimple(table_name=test_new_table, region_name=test_region, profile=test_profile)
table_list = dbsimple.list_tables()
# returns a list
```

*Creating a Table*
```
dbsimple = DynamodbSimple(region_name='region', profile='profile', table_name='table_name')
dbsimple.create_table(
    partition_key='foo',
    sort_key='bar', #optional
    throughput='5'
)
```

*Delete a table*
```
dbsimple = DynamodbSimple(region_name='region', profile='profile', table_name='table_name')
dbsimple.delete_table()
```


*Writing data in bulk*
```
dbsimple = DynamodbSimple(region_name='region', profile='profile', table_name='table_name')
dbsimple.batch_write_items(items=items) # items is a list of dicts
``` 

*Writing individual items*
```
dbsimple = DynamodbSimple(region_name='region', profile='profile', table_name='table_name')
for item in items:
    dbsimple.insert_item(item=item) #item is a dict
```

*Dynamo Query*
```
dbsimple = DynamodbSimple(region_name='region', profile='profile', table_name='table_name')
data = dbsimple.dynamo_query(
    field='foo', # field must be partition key, sort key or indexed
    value='baseball'
    )
# returns a list of dicts
```

*Dynamo Scan*
```
dbsimple = DynamodbSimple(region_name='region', profile='profile', table_name='table_name')
data = dbsimple.dynamo_scan(
    key='moo', # any key
    value='mar'
)
# returns a list of dicts
```

*Get all data*
```
dbsimple = DynamodbSimple(region_name='region', profile='profile', table_name='table_name')
all_data = dbsimple.get_all() # returns a list of dicts
```

*Delete key/value pair*
```
dbsimple = DynamodbSimple(region_name='region', profile='profile', table_name='table_name')
dbsimple.delete_item(
    key='foo', # key must be partition key, sort key or indexed
    value='giraffe'
)
```

*Update DynamoDB entry*
```
dbsimple = DynamodbSimple(region_name='region', profile='profile', table_name='table_name')
dbsimple.update_item(
    key='woo',
    value='sageing',
    id_key='foo', # key must be partition key, sort key or indexed
    id_value='yar'
)
```

### SQS

*Does a Queue Exist?*
```
sqs_simple = sqsSimple(region_name='region', profile='profile', queue_name='queue_name')
sqs_simple.queue_exists()
```

*List Queues*
```
sqs_simple = sqsSimple(region_name='region', profile='profile')
sqs_list = sqs_simple.list_queues()
# returns a list
```

*Create Queue*
```
sqs_simple = sqsSimple(region_name='region', profile='profile') 
sqs_simple.create_queue(queue='queue_name')
```

*Delete Queue*
```
sqs_simple = sqsSimple(region_name='region', profile='profile', queue='queue_name')
sqs_simple.delete_queue()
```

*Send Message*
```
sqs_simple = sqsSimple(region_name='region', profile='profile', queue='queue_name')
sqs_simple.send_sqs_message(message=message) # message is text
```

*Get Messages*
```
sqs_simple = sqsSimple(region_name='region', profile='profile', queue='queue_name')
messages = sqs_simple.get_sqs_messages(num_messages=5)
# returns a list
```

*Purge Queue*
```
sqs_simple = sqsSimple(region_name='region', profile='profile', queue='queue_name')
sqs_simple.purge_queue()
```

### SNS

*List Topics*
```
sns_simple = snsSimple(region_name='region', profile='profile')
topics = sns_simple.list_topics()
# Returns a list
```

*List Subscriptions*
```
sns_simple = snsSimple(region_name='region', profile='profile')
subscriptions = sns_simple.list_subscriptions()
# Returns a list
```

*Send Message*
```
sns_simple = snsSimple(region_name='region', profile='profile')
sns_simple.send_notification(arn='AWS Topic ARN', subject='subject', message='message')
```

### CloudFront

*List Distributions*
```
cfsimple = Cloudfront_Simple(region_name=test_region, profile=test_profile)
dists = cfsimple.cf_list()
```

*Get Details of a Distribution*
```
cfsimple = Cloudfront_Simple(region_name=test_region, profile=test_profile)
details = cfsimple.cf_details(id=cf_id)

or

details = cfsimple.cf_details(domain=domain)
    
or

details3 = cfsimple.cf_details(alias=alias)

or

details4 = cfsimple.cf_details(origin=origin)
```

*Create an Invalidation*
```
 cfsimple = Cloudfront_Simple(region_name=region, profile=profile)
 response = cfsimple.cf_invalidate(cf_id, path)
 ```

### EC2

*List Instances*

```
ec2 = ec2Simple(region_name=region, profile=test_profile)
instances = ec2.list_instances()
# Returns instance iterator
```

### Tests

There is under /tests simple_aws_tests_sample.py, with example code to test each of the services. 

### CLI

Under /cli there are two files: simple_aws_inventory_sample.py, which allows you to run an inventory of all resources under the following services: EC2 instances, S3 buckets, DynamoDB tables, SNS Topics and subscriptions, and SQS Queues under all regions. The other is simple_aws_cf_invalidation.py, **which requires the python library 'click'**, and can create an invalidation by domain name.


