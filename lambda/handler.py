import boto3
import json
from datetime import datetime
from dateutil import parser

timestream = boto3.client('timestream-write')
DATABASE_NAME = 'iot_telemetry'
TABLE_NAME = 'iot_data_items'

def lambda_handler(event, context):
    for record in event.get("Records", []):
        try:
            payload = json.loads(record.get("body", "{}"))
            data_items = payload.get("DataItems", [])
            timestamp = payload.get("Timestamp")

            timestream_records = []
            for item in data_items:
                try:
                    variable = item["Variable"]
                    value = item["Value"]
                    value_type = item["Type"]
                    quality = item.get("QualityCode", "UNKNOWN")
                    station = item.get("StationName", "UNKNOWN")
                    ts = item.get("SourceTimestamp", timestamp)

                    # Determine correct MeasureValueType
                    value_type_map = {
                        "BOOL": "BOOLEAN",
                        "INT16": "BIGINT",
                        "INT32": "BIGINT",
                        "FLOAT": "DOUBLE",
                        "DOUBLE": "DOUBLE"
                    }
                    measure_type = value_type_map.get(value_type.upper(), "VARCHAR")

                    timestream_records.append({
                        'Dimensions': [
                            {'Name': 'Station', 'Value': station},
                            {'Name': 'Variable', 'Value': variable},
                            {'Name': 'QualityCode', 'Value': quality}
                        ],
                        'MeasureName': variable,
                        'MeasureValue': str(value),
                        'MeasureValueType': measure_type,
                        'Time': str(int(parser.parse(ts).timestamp() * 1000)),
                        'TimeUnit': 'MILLISECONDS'
                    })

                except Exception as item_error:
                    print(f"Skipping item due to error: {item_error}")

            if timestream_records:
                timestream.write_records(
                    DatabaseName=DATABASE_NAME,
                    TableName=TABLE_NAME,
                    Records=timestream_records
                )
                print(f"Wrote {len(timestream_records)} records to Timestream")

        except Exception as e:
            print(f"Error processing record: {e}")

    return {"statusCode": 200, "body": "Write successful"}