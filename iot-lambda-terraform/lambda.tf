# Lambda Function Definition
resource "aws_lambda_function" "iot_handler" {
  function_name    = "iot_lambda_handler"
  role             = aws_iam_role.lambda_exec.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.11"
  source_code_hash = filebase64sha256("../lambda.zip")
  filename         = "../lambda.zip"
  timeout          = 10

  environment {
    variables = {
      PG_HOST = "dummy"
    }
  }
}

# IoT Topic Rule to Listen to Both T0 and T1 Topics
resource "aws_iot_topic_rule" "iot_rule" {
  name        = "iot_to_lambda"
  enabled     = true

  sql         = "SELECT * FROM 'T0' UNION SELECT * FROM 'T1'"
  sql_version = "2016-03-23"

  lambda {
    function_arn = aws_lambda_function.iot_handler.arn
  }
}

# Lambda Permission to Allow IoT Rule Invocation
resource "aws_lambda_permission" "allow_iot" {
  statement_id  = "AllowExecutionFromIoT"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.iot_handler.function_name
  principal     = "iot.amazonaws.com"
  source_arn    = aws_iot_topic_rule.iot_rule.arn
}