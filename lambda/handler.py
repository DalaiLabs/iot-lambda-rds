import boto3
import json
from datetime import datetime

DATABASE_NAME = 'iot_telemetry'
TABLE_NAME = 'iot_data_items'

timestream = boto3.client('timestream-write')


def map_type(datatype):
    t = datatype.upper()
    if t in ["DOUBLE", "FLOAT"]:
        return "DOUBLE"
    if t in ["INT", "INT16", "INT32", "INT64", "LONG"]:
        return "BIGINT"
    if t in ["BOOL", "BOOLEAN"]:
        return "BOOLEAN"
    return "VARCHAR"


def lambda_handler(event, context):
    try:
        payload = json.loads(event['body']) if 'body' in event else event
        data_items = payload.get("DataItems", [])
        timestamp = payload.get("Timestamp")

        if not data_items or not timestamp:
            print("Invalid payload: Missing DataItems or Timestamp.")
            return {"statusCode": 400, "body": "Invalid payload"}

        records = []
        for item in data_items:
            value_type = item.get("Type", "VARCHAR")
            value = str(item.get("Value"))
            station = item.get("StationName", "unknown")
            variable = item.get("Variable", "unknown")
            quality = item.get("QualityCode", "UNKNOWN")
            source_time = item.get("SourceTimestamp", timestamp)

            records.append({
                'Dimensions': [
                    {'Name': 'Station', 'Value': station, 'DimensionValueType': 'VARCHAR'},
                    {'Name': 'Variable', 'Value': variable, 'DimensionValueType': 'VARCHAR'},
                    {'Name': 'QualityCode', 'Value': quality, 'DimensionValueType': 'VARCHAR'}
                ],
                'MeasureName': variable,
                'MeasureValue': value,
                'MeasureValueType': map_type(value_type),
                'Time': str(int(datetime.fromisoformat(source_time).timestamp() * 1000)),
                'TimeUnit': 'MILLISECONDS'
            })

        result = timestream.write_records(
            DatabaseName=DATABASE_NAME,
            TableName=TABLE_NAME,
            Records=records
        )
        print("Write result:", result)

    except Exception as e:
        print(f"Error writing to Timestream: {e}")
        return {"statusCode": 500, "body": "Failed to write to Timestream"}

    return {"statusCode": 200, "body": "Success"}