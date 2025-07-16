import boto3
import json
from datetime import datetime

DATABASE_NAME = 'iot_telemetry'
TABLE_NAME = 'iot_data_items'

timestream = boto3.client('timestream-write')

def lambda_handler(event, context):
    print("🔁 Lambda triggered.")

    try:
        # Parse payload
        payload = json.loads(event['body']) if 'body' in event else event
        print("✅ Payload parsed.")

        # Extract timestamp
        timestamp_str = payload.get("Timestamp")
        try:
            timestamp_ms = str(int(datetime.fromisoformat(timestamp_str).timestamp() * 1000))
            print(f"⏱️ Timestamp parsed from payload: {timestamp_ms}")
        except Exception:
            timestamp_ms = str(int(datetime.utcnow().timestamp() * 1000))
            print(f"⚠️ Fallback to current UTC time: {timestamp_ms}")

        # Process DataItems
        data_items = payload.get("DataItems", [])
        data_items = data_items[:100]  # Timestream record limit
        print(f"📦 Found {len(data_items)} data items.")

        records = []

        for item in data_items:
            variable = item.get("Variable", "unknown")
            value = item.get("Value", 0)
            var_type = item.get("Type", "DOUBLE")
            station = item.get("StationName", "unknown")
            quality = item.get("QualityCode", "UNKNOWN")

            # Skip invalid values (like list type)
            if isinstance(value, list):
                print(f"⛔ Skipping {variable} due to invalid list value: {value}")
                continue

            # Determine MeasureValueType and safely cast value
            try:
                if var_type.upper() in ["INT", "INT16", "INT32", "INT64"]:
                    measure_value_type = "BIGINT"
                    value = str(int(value))
                elif var_type.upper() == "BOOL":
                    measure_value_type = "BOOLEAN"
                    value = str(bool(value)).lower()
                elif var_type.upper() in ["FLOAT", "DOUBLE"]:
                    measure_value_type = "DOUBLE"
                    value = str(float(value))
                else:
                    measure_value_type = "VARCHAR"
                    value = str(value)
            except Exception as ve:
                print(f"⚠️ Skipping {variable} due to value casting error: {ve}")
                continue

            print(f"🧪 {variable} = {value} ({measure_value_type})")

            records.append({
                'Dimensions': [
                    {'Name': 'Station', 'Value': station, 'DimensionValueType': 'VARCHAR'},
                    {'Name': 'Variable', 'Value': variable, 'DimensionValueType': 'VARCHAR'},
                    {'Name': 'QualityCode', 'Value': quality, 'DimensionValueType': 'VARCHAR'}
                ],
                'MeasureName': variable,
                'MeasureValue': value,
                'MeasureValueType': measure_value_type,
                'Time': timestamp_ms,
                'TimeUnit': 'MILLISECONDS'
            })

        print(f"📝 Prepared {len(records)} records for writing to Timestream.")

        # Write to Timestream
        if records:
            timestream.write_records(
                DatabaseName=DATABASE_NAME,
                TableName=TABLE_NAME,
                Records=records
            )
            print("✅ Records successfully written to Timestream.")

        return {"statusCode": 200, "body": "Data written to Timestream"}

    except Exception as e:
        print(f"❌ Error writing to Timestream: {e}")
        return {"statusCode": 500, "body": f"Failed: {str(e)}"}