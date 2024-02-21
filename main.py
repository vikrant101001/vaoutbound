import os
import tempfile
import boto3
import random
import string
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Define the S3 bucket and key directly
        s3_bucket = "naii-01-dir"
        s3_key = "01-028/test_" + ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + ".docx"

        # Set up AWS credentials directly
        aws_access_key_id = os.environ["aws_access_key_id"]
        aws_secret_access_key = os.environ["aws_secret_access_key"]
        aws_region = "us-east-1"

        # Generate random content for the .docx file
        content = ''.join(random.choices(string.ascii_letters + string.digits, k=1000))

        # Create a new temporary file for the .docx document
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp_file:
            tmp_file.write(content.encode())
            tmp_file_path = tmp_file.name

        # Upload the document to S3
        s3 = boto3.client("s3", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)
        s3.upload_file(tmp_file_path, s3_bucket, s3_key)

        # Delete the temporary file
        os.unlink(tmp_file_path)

        return func.HttpResponse("Random document uploaded successfully to S3!", status_code=200)
    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
