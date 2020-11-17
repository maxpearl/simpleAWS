"""
Simple_aws S3 Functions

"""
import boto3
import io

class S3Simple(object):

    def __init__(self, **kwargs):
        """
        Initializes S3 connection & bucket
        """
        if 'region_name' in kwargs:
            self.region_name = kwargs['region_name']

        if 'profile' in kwargs:
            profile = kwargs['profile']

        session = boto3.session.Session(profile_name=profile,
                                    region_name=self.region_name)
        self.s3 = session.resource('s3')

        if 'bucket_name' in kwargs:
            self.bucket_name = kwargs['bucket_name']
            self.bucket = self.s3.Bucket(kwargs['bucket_name'])

        return

    def list_buckets(self):
        """
        Return a list of all S3 buckets in a client region
        """
        bucket_iterator = self.s3.buckets.all()

        bucket_names = []
        for bucket in bucket_iterator:
            bucket_names.append(bucket.name)

        return (bucket_names)

    def s3_bucket_contents(self, **kwargs):
        """
        Return a list of all contents of a bucket
        """
        object_summary_iterator = self.bucket.objects.all()

        s3_list = []
        try:
            for s3_object in object_summary_iterator:
                s3_list.append(s3_object.key)
            return s3_list
        except:
            return False

    def s3_bucket_filter(self, **kwargs):
        """
        List contents of bucket with a filter
        """
        if 'max-keys' in kwargs.keys():
            max_keys = kwargs['max_keys']
        else:
            max_keys = 1000 #S3 API default
        
        if 'prefix' not in kwargs.keys():
            return False

        object_summary_iterator = self.bucket.objects.filter(
            Prefix=kwargs['prefix'],
            MaxKeys=max_keys
        )

        s3_list = []
        for s3_object in object_summary_iterator:
            s3_list.append(s3_object.key)

        return s3_list

    def download_file(self, **kwargs):
        """
        Download a file from S3
        """
        obj = self.bucket.Object(kwargs['file_name'])

        with open(kwargs['output_file'], 'wb') as data:
            obj.download_fileobj(data)
        
        return

    def delete_s3_file(self, **kwargs):
        """
        Deletes a file in an s3 bucket
        """
        obj = self.bucket.Object(kwargs['file_name'])

        #delete object
        obj.delete()
        return

    def s3_new_bucket(self):
        """
        Create new S3 bucket
        """
        if self.region_name != 'us-east-1':
            self.bucket = self.s3.create_bucket(
                ACL='private',
                Bucket=self.bucket_name,
                CreateBucketConfiguration={
                                'LocationConstraint': self.region_name
                            }
            )
        else:
            self.bucket = self.s3.create_bucket(
                ACL='private',
                Bucket=self.bucket_name
            )

        return

    def s3_delete_bucket(self):
        """
        Delete Bucket
        """
        self.bucket.delete()

        return

    def put_to_s3(self, **kwargs):
        """
        Save string to file in S3
        """
        if 'body' not in kwargs:
            return False

        fake_handle = io.StringIO(kwargs['body'])
        self.bucket.put_object(
            Key=kwargs['key'],
            Body=fake_handle.read()
        )
        
        return

    def send_file_to_s3(self,**kwargs):
        """
        Sends local file to an S3 bucket
        """
        if 'local_file' not in kwargs or 's3_file' not in kwargs:
            return False

        extra_args = None
        if 'public' in kwargs:
            if kwargs['public']:
                extra_args = {'ACL': 'public-read'}
        # upload to s3
        self.s3.Bucket(self.bucket_name).upload_file(
            kwargs['local_file'], kwargs['s3_file'], ExtraArgs=extra_args
            )
        
        return True
