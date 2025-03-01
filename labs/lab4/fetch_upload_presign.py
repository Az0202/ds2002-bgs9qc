#!/usr/bin/env python3
import sys
import requests
import boto3

if len(sys.argv) != 4:
    print("Usage: python fetch_upload_presign.py <file_url> <bucket_name> <expires_in_seconds>")
    sys.exit(1)

file_url = sys.argv[1]
bucket_name = sys.argv[2]
expires_in = int(sys.argv[3])

# Extract filename from the URL
filename = file_url.split('/')[-1]

# 1. Fetch the file from the internet
resp = requests.get(file_url)
if resp.status_code != 200:
    print(f"Failed to download file. Status code: {resp.status_code}")
    sys.exit(1)

with open(filename, 'wb') as f:
    f.write(resp.content)

print(f"Downloaded {filename}")

# 2. Upload to S3 (private by default)
s3_client = boto3.client('s3', region_name='us-east-1')
with open(filename, 'rb') as data:
    s3_client.put_object(
        Bucket=bucket_name,
        Key=filename,
        Body=data
    )

print(f"Uploaded {filename} to {bucket_name}")

# 3. Generate a presigned URL
presigned_url = s3_client.generate_presigned_url(
    'get_object',
    Params={'Bucket': bucket_name, 'Key': filename},
    ExpiresIn=expires_in
)

print("Presigned URL:", presigned_url)
