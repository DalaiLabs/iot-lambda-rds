import boto3

def lambda_handler(event, context):
    try:
        timestream = boto3.client('timestream-write')
        response = timestream.describe_database(DatabaseName='iot_telemetry')
        print("✅ Connected to Timestream. Database info:")
        print(response)
        return {
            "statusCode": 200,
            "body": "Successfully connected to Timestream."
        }
    except Exception as e:
        print("❌ Failed to connect:", str(e))
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }