"""
Dynamodb functions library

Super simplified AWS functions.
"""
import boto3
from boto3.dynamodb.conditions import Key, Attr

class DynamodbSimple(object):

    def __init__(self, **kwargs):
        """
        Initializes DynamoDB object
        :param: kwargs: [table_name]: DynamoDB table being operated on
                        region_name: AWS region
                        profile: AWS profile
        """
        if 'region_name' in kwargs:
            region_name = kwargs['region_name']

        if 'profile' in kwargs:
            profile = kwargs['profile']
        
        session = boto3.session.Session(profile_name=profile, region_name=region_name)
        self.dynamodb = session.resource('dynamodb')

        if 'table_name' in kwargs:
            self.table_name = kwargs['table_name']
            self.table = self.dynamodb.Table(kwargs['table_name'])

        return

    def check_table(self):
        """
        check_table: 
        Function to check  if a table exists
        """
        try:
            self.table.creation_date_time
            return True
        except:
            return False

    def list_tables(self):

        table_iterator = self.dynamodb.tables.all()

        dynamodb_tables = []
        for table in table_iterator:
            try:
                for table in table_iterator:
                    dynamodb_tables.append(table.name)
                return dynamodb_tables
            except:
                return False

    def create_table(self, **kwargs):
        """
        This creates a new table in Dynamo
        :param: kwargs: partition_key
                        sort_key
                        throughput
        """
        if 'partition_key' not in kwargs:
            return False
        
        partition_key = kwargs['partition_key']
        if 'sort_key' in kwargs.keys():
            sort_key = kwargs['sort_key']
        else:
            sort_key = ''
        if 'throughput' in kwargs.keys():
            throughput = kwargs['throughput']
        else:
            throughput = '5'
        
        throughput = int(throughput)
        
        if not sort_key:
            new_table = self.dynamodb.create_table(
                AttributeDefinitions=[
                    {
                        'AttributeName' : partition_key,
                        'AttributeType' : 'S',
                    },
                ],
                KeySchema=[
                    {
                        'AttributeName' : partition_key,
                        'KeyType' : 'HASH',
                    },
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': throughput,
                    'WriteCapacityUnits': throughput,
                },
                TableName=self.table_name,
            )
        else: # has sort_key:
            new_table = self.dynamodb.create_table(
                AttributeDefinitions=[
                    {
                        'AttributeName' : partition_key,
                        'AttributeType' : 'S',
                    },
                    {
                        'AttributeName' : sort_key,
                        'AttributeType' : 'S',
                    }
                ],
                KeySchema=[
                    {
                        'AttributeName' : partition_key,
                        'KeyType' : 'HASH',
                    },
                    {
                        'AttributeName' : sort_key,
                        'KeyType' : 'RANGE',
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': throughput,
                    'WriteCapacityUnits': throughput,
                },
                TableName=self.table_name,
            )
        
        new_table.wait_until_exists()
        return

    def delete_table(self):
        """
        Delete Dynamodb Table
        """
        self.table.delete()

        return

    def dynamo_query(self, **kwargs):
        """
        Query a dynamo table
        """
        
        field = kwargs['field']              # field to query (must be queryable)
        value = kwargs['value']              # value to query on the field
        if 'sort_key' in kwargs.keys():
            sort_key = kwargs['sort_key']        # (optional) sort key
            sort_value = kwargs['sort_value']    # (optional) sort value
        else:
            sort_key = ''
            sort_value = ''

        if not sort_key:
            response = self.table.query(KeyConditionExpression=Key(field).eq(value))
        else:
            response = self.table.query(KeyConditionExpression=Key(field).eq(value) & Key(sort_key).eq(sort_value))
                
        if int(response['Count']) == 0:  # no items returned
            return {}
        else:
            return response['Items']

    def dynamo_scan(self, **kwargs):
        """
        Scans a dynamo table for a particular key-value pair
        """
        response = self.table.scan(
            FilterExpression=Key(kwargs['key']).eq(kwargs['value'])
        )

        return response['Items']

    def get_all(self):
        """
        Function to grab all rows from a big dynamo table
        """
        response = self.table.scan()
        
        data = response['Items']

        while 'LastEvaluatedKey' in response:
            response = self.table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
    
        return data

    def insert_item(self, **kwargs):
        """
        This inserts an item into a dynamo table, possibly conditionally.
        If there are no conditional fields, it just puts the item,
        otherwise, it depends on an index for that conditional field.
        :param: kwargs: item: item to be inserted
        """
        if 'item' not in kwargs:
            return False

        item = kwargs['item']
        self.table.put_item(Item=item)

        return True

    def delete_item(self, **kwargs):
        """
        Function to delete item in dynamo table
        """

        if 'key' not in kwargs or 'value' not in kwargs:
            return False

        self.table.delete_item(
            Key={
                kwargs['key'] : kwargs['value']
            },
        )
        
        return 

    def update_item(self, **kwargs):
        """
        This updates a particular item in a dynamo table, adding a new key value pair.
        """
        if 'key' not in kwargs or 'value' not in kwargs:
            return False
        if 'id_key' not in kwargs or 'id_value' not in kwargs:
            return False

        self.table.update_item(
            ExpressionAttributeNames={
                '#K' : kwargs['key']
            },
            ExpressionAttributeValues={
                ':k' : kwargs['value']
            },
            Key={
                kwargs['id_key'] : kwargs['id_value']
            },
            ReturnValues='ALL_NEW',
            TableName=self.table_name,
            UpdateExpression='SET #K = :k',
        )

        return True

    def batch_write_items(self,**kwargs):
        """
        This uses DynamoDB's batch write function to write a bunch of items
        :params: kwargs: [items]: items to write
        """
        if 'items' not in kwargs:
            return False

        with self.table.batch_writer() as batch:
            for item in kwargs['items']:
                batch.put_item(Item=item)

        return True