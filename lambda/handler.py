import boto3
from datetime import datetime

DATABASE_NAME = 'iot_telemetry'
TABLE_NAME = 'iot_data_items'
timestream = boto3.client('timestream-write')

def lambda_handler(event, context):
    print("Starting Timestream test write...")

    try:
        response = timestream.write_records(
            DatabaseName=DATABASE_NAME,
            TableName=TABLE_NAME,
            Records=[
                {
                    'Dimensions': [
                        {'Name': 'Station', 'Value': 'T1'},
                        {'Name': 'Variable', 'Value': 'temperature'},
                        {'Name': 'QualityCode', 'Value': 'GOOD'}
                    ],
                    'MeasureName': 'temperature',
                    'MeasureValue': '24.7',
                    'MeasureValueType': 'DOUBLE',
                    'Time': str(int(datetime.utcnow().timestamp() * 1000)),
                    'TimeUnit': 'MILLISECONDS'
                }
            ]
        )
        print("✅ Write success:", response)
        return {"statusCode": 200, "body": "Sample data written to Timestream"}

    except Exception as e:
        print("❌ Error writing to Timestream:", str(e))
        return {"statusCode": 500, "body": f"Write error: {str(e)}"}