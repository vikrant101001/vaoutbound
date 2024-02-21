import os
import random
import boto3
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Define the S3 bucket and key directly
        s3_bucket = "naii-01-dir"
        s3_key = "01-028/test.docx"

        # Set up AWS credentials directly
        aws_access_key_id = os.environ["aws_access_key_id"]
        aws_secret_access_key = os.environ["aws_secret_access_key"]
        aws_region = "us-east-1"

        # Fetch a random document from the S3 bucket (replace this logic with your own)
        s3 = boto3.client("s3", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)
        # List all objects in the bucket
        objects = s3.list_objects(Bucket=s3_bucket)['Contents']
        # Choose a random object key
        random_object_key = random.choice(objects)['Key']

        # Upload the random document to another location within the same bucket
        s3.copy_object(Bucket=s3_bucket, Key=s3_key, CopySource={'Bucket': s3_bucket, 'Key': random_object_key})

        return func.HttpResponse("File uploaded to S3 successfully", status_code=200)
    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
