# SimpleAWS

Version 0.1.3

Simplified Libraries for some of the most common AWS resources. The purpose of SimpleAWS is to add one layer of abstraction, and remove a lot of the guess-work from interfacing with some AWS resources.

The options are limited on purpose - this is *not* designed to replace boto3, but to provide an easier entry into using AWS resources with python.

## AWS Requirements

SimpleAWS uses profiles and secret/access keys. Put a file called 'credentials' inside the .aws directory in your home directory (the home of the user running this code.) The format of the file is:
[profilename]
aws_access_key_id = <key>
aws_secret_access_key = <key>

## Installation

`pip install simple-aws`

## Usage

```
from dynamodb_functions import *
from s3_functions import *
from sns_functions import *
from sqs_functions import *
```

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

*Delete File*
```
s3simple = S3Simple(region_name='region', profile='profile', bucket_name='bucket-name')
s3simple.delete_s3_file(file_name=key)
```

*Delete Bucket*
```
s3simple = S3Simple(region_name='region', profile='profile', bucket_name='bucket-name')
s3simple.s3_delete_bucket()
```

### DynamoDB

*Checking to see if a table exists*
```
dbsimple = DynamodbSimple(table_name='table_name', region_name='region', profile='profile') 
# region and profile are optional
if dbsimple.check_table(): # returns True/False
    ...

```

*Creating Table*
```
dbsimple = DynamodbSimple(region_name='region', profile='profile', table_name='table_name')
dbsimple.create_table(
    partition_key='foo',
    sort_key='bar', #optional
    throughput='5'
)
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

*Delete DynamoDB table*
```
dbsimple = DynamodbSimple(region_name='region', profile='profile', table_name='table_name')
dbsimple.delete_table()
```

### SQS

*Does a Queue Exist?*
```
sqs_simple = sqsSimple(region_name='region', profile='profile', queue_name='queue_name')
sqs_simple.queue_exists()
```

*Create Queue*
```
sqs_simple = sqsSimple(region_name='region', profile='profile') 
sqs_simple.create_queue(queue='queue_name')
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

*Delete Queue*
```
sqs_simple = sqsSimple(region_name='region', profile='profile', queue='queue_name')
sqs_simple.delete_queue()
```

### SNS

*Send Message*
```
sns_simple = snsSimple(region_name='region', profile='profile')
sns_simple.send_notification(arn='AWS Topic ARN', subject='subject', message='message')
```


