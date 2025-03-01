#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <local_file> <bucket_name> <expires_in_seconds>"
    exit 1
fi

LOCAL_FILE=$1
BUCKET_NAME=$2
EXPIRATION=$3

# 1. Upload the file (private by default)
aws s3 cp "$LOCAL_FILE" s3://"$BUCKET_NAME"/

# 2. Generate and print a presigned URL
PRESIGNED_URL=$(aws s3 presign s3://"$BUCKET_NAME"/"$LOCAL_FILE" --expires-in "$EXPIRATION")
echo "Presigned URL: $PRESIGNED_URL"

