import boto3
import datetime
from botocore.exceptions import ClientError

s3 = boto3.client('s3')
s3_resource = boto3.resource('s3')
ec2 = boto3.client('ec2')

def list_buckets():
    response = s3.list_buckets()
    buckets = []
    for b in response.get('Buckets', []):
        b_copy = b.copy()
        b_copy['CreationDate'] = b_copy['CreationDate'].isoformat() if isinstance(b_copy['CreationDate'], datetime.datetime) else b_copy['CreationDate']
        buckets.append(b_copy)
    return buckets

def create_bucket(bucket_name):
    bucket_name = bucket_name.lower()
    region = s3.meta.region_name
    if region == 'us-east-1':
        s3.create_bucket(Bucket=bucket_name)
    else:
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': region})

def delete_bucket(bucket_name):
    bucket = s3_resource.Bucket(bucket_name)
    bucket.object_versions.delete()
    bucket.delete()

def list_ec2_instances():
    response = ec2.describe_instances()
    instances = []
    for res in response.get('Reservations', []):
        for inst in res.get('Instances', []):
            inst_copy = {
                'InstanceId': inst.get('InstanceId'),
                'State': inst.get('State', {}).get('Name'),
                'PublicIp': inst.get('PublicIpAddress'),
                'PrivateIp': inst.get('PrivateIpAddress')
            }
            instances.append(inst_copy)
    return instances

def upload_file(bucket_name, file_obj, filename):
    try:
        s3.upload_fileobj(file_obj, bucket_name, filename, ExtraArgs={'ACL':'public-read'})
        region = s3.meta.region_name
        url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{filename}"
        return url
    except ClientError as e:
        raise e
