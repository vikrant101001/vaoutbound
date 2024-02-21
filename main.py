import os
import tempfile
import boto3
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        file_data = req_body.get('file_data')
        s3_bucket = req_body.get('s3_bucket')
        s3_key = req_body.get('s3_key')

        if not file_data or not s3_bucket or not s3_key:
            return func.HttpResponse("Missing required parameters", status_code=400)

        # Set up AWS credentials directly
        aws_access_key_id = os.environ["aws_access_key_id"]
        aws_secret_access_key = os.environ["aws_secret_access_key"]
        aws_region = "us-east-1"

        # Save the file content to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(base64.b64decode(file_data))
            tmp_file_path = tmp_file.name

        # Upload file to S3
        s3 = boto3.client("s3", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)
        s3.upload_file(tmp_file_path, s3_bucket, s3_key)

        # Delete the temporary file
        os.unlink(tmp_file_path)

        return func.HttpResponse("File uploaded to S3 successfully", status_code=200)
    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
