import boto3
import os
import json
from datetime import datetime

DATABASE_NAME = 'iot_telemetry'
TABLE_NAME = 'iot_data_items'
timestream = boto3.client('timestream-write')


def lambda_handler(event, context):
    try:
        # Parse event if it's a JSON string
        payload = event if isinstance(event, dict) else json.loads(event)

        data_items = payload.get('DataItems')
        if not data_items:
            print("❌ No 'DataItems' key found in the payload.")
            return {"statusCode": 400, "body": "Missing DataItems"}

        records = []

        for item in data_items:
            try:
                # Extract fields
                variable = item['Variable']
                value = item['Value']
                value_type = item['Type']
                station = item['StationName']
                quality = item.get('QualityCode', 'UNKNOWN')
                timestamp = item.get('SourceTimestamp') or payload.get('Timestamp')

                # Determine Timestream measure value type
                if value_type == 'BOOL':
                    measure_value_type = 'BIGINT'
                elif value_type in ['INT16', 'INT32', 'INT']:
                    measure_value_type = 'BIGINT'
                elif value_type in ['FLOAT', 'DOUBLE', 'DECIMAL']:
                    measure_value_type = 'DOUBLE'
                else:
                    measure_value_type = 'VARCHAR'

                # Convert ISO timestamp to epoch ms
                epoch_ms = int(datetime.fromisoformat(timestamp).timestamp() * 1000)

                records.append({
                    'Dimensions': [
                        {'Name': 'Station', 'Value': station},
                        {'Name': 'Variable', 'Value': variable},
                        {'Name': 'QualityCode', 'Value': quality}
                    ],
                    'MeasureName': variable,
                    'MeasureValue': str(value),
                    'MeasureValueType': measure_value_type,
                    'Time': str(epoch_ms),
                    'TimeUnit': 'MILLISECONDS'
                })

            except Exception as item_error:
                print(f"⚠️ Skipping item due to error: {item} → {item_error}")

        if not records:
            print("⚠️ No valid records to write to Timestream.")
            return {"statusCode": 204, "body": "No valid records"}

        # Write to Timestream
        response = timestream.write_records(
            DatabaseName=DATABASE_NAME,
            TableName=TABLE_NAME,
            Records=records
        )
        print(f"✅ Successfully wrote {len(records)} records to Timestream.")
        return {"statusCode": 200, "body": json.dumps(response)}

    except Exception as e:
        print(f"❌ Lambda failed with error: {e}")
        return {"statusCode": 500, "body": str(e)}