
# IoT Telemetry Ingestion Pipeline using AWS Lambda and Timestream

This project sets up an AWS-based serverless pipeline to ingest IoT telemetry data into Amazon Timestream for analytics and time-series analysis.

## Architecture

```
IoT Device → AWS IoT Rule → AWS Lambda → Amazon Timestream
```

- **AWS IoT** receives telemetry messages.
- **AWS Lambda** processes and transforms the incoming messages.
- **Amazon Timestream** stores the data for querying and analytics.

## Folder Structure

```
├── lambda/                     # Python Lambda function
│   └── handler.py              # Main Lambda logic
│   └── requirements.txt        # Python dependencies
├── iot-lambda-terraform/      # Terraform infrastructure
│   ├── main.tf                 # Main resources
│   ├── iam.tf                  # IAM Role and policies
│   └── variables.tf            # Input variables
├── lambda.zip                 # Zipped Lambda code for deployment
├── .github/workflows/terraform.yml  # GitHub Actions CI/CD workflow
└── README.md
```

## Setup Instructions

### 1. Terraform Infrastructure Deployment

Update your Terraform backend configuration (`main.tf`) and IAM role setup (`iam.tf`) to:

- Create IAM roles and attach policies
- Deploy the Lambda function
- Set up permissions for IoT → Lambda and Lambda → Timestream

Run:

```bash
cd iot-lambda-terraform
terraform init
terraform apply -auto-approve
```

### 2. Lambda Function Details

- Located in `lambda/handler.py`
- Parses `DataItems` payloads in JSON with timestamp, variable, and station info
- Converts and writes data into Timestream

Example payload:
```json
{
  "Timestamp": "2025-07-16T18:54:02",
  "DataItems": [
    {
      "Variable": "AccumulatorValve",
      "Type": "BOOL",
      "Value": 0,
      "QualityCode": "GOOD",
      "StationName": "PLC_3_Main_Control_Room_T1"
    }
  ]
}
```

### 3. Deployment via GitHub Actions

CI/CD pipeline is triggered on push to `main` branch. It performs:

- Python setup
- Lambda zipping
- Terraform provisioning


### 4. Todo
- Put all the PLCs in the pipeline 
- Set the sync time to every 1h 
- Aggregate, show in the Engineering Dashboard
