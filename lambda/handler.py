import boto3
import json
from datetime import datetime

DATABASE_NAME = 'iot_telemetry'
TABLE_NAME = 'iot_data_items'
timestream = boto3.client('timestream-write')

def lambda_handler(event, context):
    records = event.get('Records')
    if not records:
        print("No 'Records' key found in the event.")
        return {"statusCode": 400, "body": "Invalid event structure"}

    for record in records:
        try:
            payload = json.loads(record['body']) if 'body' in record else json.loads(record['payload'])

            variable = payload.get('Variable')
            value = str(payload.get('Value'))
            station = payload.get('StationName', 'unknown')
            quality = payload.get('QualityCode', 'UNKNOWN')

            timestream.write_records(
                DatabaseName=DATABASE_NAME,
                TableName=TABLE_NAME,
                Records=[
                    {
                        'Dimensions': [
                            {'Name': 'Station', 'Value': station},
                            {'Name': 'Variable', 'Value': variable},
                            {'Name': 'QualityCode', 'Value': quality}
                        ],
                        'MeasureName': variable,
                        'MeasureValue': value,
                        'MeasureValueType': 'DOUBLE',
                        'Time': str(int(datetime.utcnow().timestamp() * 1000)),  # in ms
                        'TimeUnit': 'MILLISECONDS'
                    }
                ]
            )
        except Exception as e:
            print(f"Error processing record: {e}")

    return {"statusCode": 200}