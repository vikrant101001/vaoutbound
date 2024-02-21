import boto3
import json
from azure.functions import HttpRequest, HttpResponse

def main(req: HttpRequest) -> HttpResponse:
    try:
        req_body = req.get_json()
        file_path = req_body.get('file_path')
        s3_bucket = req_body.get('s3_bucket')
        s3_key = req_body.get('s3_key')

        if not file_path or not s3_bucket or not s3_key:
            return HttpResponse("Missing required parameters", status_code=400)

        # Set up AWS credentials directly
        aws_access_key_id = os.environ["aws_access_key_id"]
        aws_secret_access_key = os.environ["aws_secret_access_key"]
        aws_region = "us-east-1"

        # Upload file to S3
        s3 = boto3.client("s3", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)
        s3.upload_file(file_path, s3_bucket, s3_key)

        return HttpResponse("File uploaded to S3 successfully", status_code=200)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status_code=500)
