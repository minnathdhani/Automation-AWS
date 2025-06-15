import boto3
import re
from datetime import datetime, timedelta, timezone

s3 = boto3.client('s3')

BUCKET_NAME = 'minnath-lambda-s3-cleanup-bucket'  # replace with your bucket name
DAYS_OLD = 30

def lambda_handler(event, context):
    now = datetime.now(timezone.utc)
    cutoff_date = now - timedelta(days=DAYS_OLD)

    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    if 'Contents' not in response:
        print("No files found in bucket.")
        return

    for obj in response['Contents']:
        key = obj['Key']
        
        # Example: extract date from 'report_2024-04-01.txt'
        match = re.search(r'(\d{4}-\d{2}-\d{2})', key)
        if match:
            try:
                file_date = datetime.strptime(match.group(1), "%Y-%m-%d").replace(tzinfo=timezone.utc)
                if file_date < cutoff_date:
                    print(f"Deleting old file: {key}")
                    s3.delete_object(Bucket=BUCKET_NAME, Key=key)
            except ValueError:
                print(f"Skipping file with invalid date format: {key}")
        else:
            print(f"No date found in filename: {key}")
