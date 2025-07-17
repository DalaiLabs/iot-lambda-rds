# Lambda Function
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

# IoT Rule for Topic T0
resource "aws_iot_topic_rule" "iot_rule_t0" {
  name        = "iot_to_lambda_t0"
  enabled     = true
  sql         = "SELECT * FROM 'T0'"
  sql_version = "2016-03-23"

  lambda {
    function_arn = aws_lambda_function.iot_handler.arn
  }
}

resource "aws_lambda_permission" "allow_iot_t0" {
  statement_id  = "AllowExecutionFromIoTT0"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.iot_handler.function_name
  principal     = "iot.amazonaws.com"
  source_arn    = aws_iot_topic_rule.iot_rule_t0.arn
}

# IoT Rule for Topic T1
resource "aws_iot_topic_rule" "iot_rule_t1" {
  name        = "iot_to_lambda_t1"
  enabled     = true
  sql         = "SELECT * FROM 'T1'"
  sql_version = "2016-03-23"

  lambda {
    function_arn = aws_lambda_function.iot_handler.arn
  }
}

resource "aws_lambda_permission" "allow_iot_t1" {
  statement_id  = "AllowExecutionFromIoTT1"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.iot_handler.function_name
  principal     = "iot.amazonaws.com"
  source_arn    = aws_iot_topic_rule.iot_rule_t1.arn
}