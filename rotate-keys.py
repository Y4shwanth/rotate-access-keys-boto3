import boto3
import json

# Set S3 bucket and file details
S3_BUCKET = "to-be-deleted-cp"
S3_FILE_PATH = "keys"

# List of IAM users to rotate access keys for
USERS = ["dummy_user1", "dummy_user2" ]

# Create a session with the specified region
session = boto3.Session(region_name="region")

# Create an IAM client using the session
iam_client = session.client("iam")

# Create an S3 client using the session
s3_client = session.client("s3")

# Iterate over the list of users
for user in USERS:
    # Generate a new access key for the current user
    new_key_response = iam_client.create_access_key(UserName=user)

    # Extract the new access key details
    new_access_key_id = new_key_response["AccessKey"]["AccessKeyId"]
    new_secret_access_key = new_key_response["AccessKey"]["SecretAccessKey"]

    # Update the AWS CLI configuration with the new access key
    boto3.setup_default_session(aws_access_key_id=new_access_key_id, aws_secret_access_key=new_secret_access_key)

    # Deactivate the old access key for the current user
    old_access_key_response = iam_client.list_access_keys(UserName=user)
    old_access_key_id = old_access_key_response["AccessKeyMetadata"][0]["AccessKeyId"]
    iam_client.update_access_key(AccessKeyId=old_access_key_id, Status="Inactive", UserName=user)

    # Clean up old access keys (optional)
    iam_client.delete_access_key(AccessKeyId=old_access_key_id, UserName=user)

    # Create a JSON object with the new access keys
    keys_json = {
        "AccessKeyId": new_access_key_id,
        "SecretAccessKey": new_secret_access_key
    }

    # Upload the JSON object to S3
    s3_client.put_object(Body=json.dumps(keys_json), Bucket=S3_BUCKET, Key=f"{S3_FILE_PATH}/{user}.json")

    print(f"Access key rotation complete for user: {user}"
