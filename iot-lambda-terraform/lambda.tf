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

# IoT Rule for Topic T3
resource "aws_iot_topic_rule" "iot_rule_t3" {
  name        = "iot_to_lambda_t3"
  enabled     = true
  sql         = "SELECT * FROM 'T3'"
  sql_version = "2016-03-23"

  lambda {
    function_arn = aws_lambda_function.iot_handler.arn
  }
}

resource "aws_lambda_permission" "allow_iot_t3" {
  statement_id  = "AllowExecutionFromIoTT3"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.iot_handler.function_name
  principal     = "iot.amazonaws.com"
  source_arn    = aws_iot_topic_rule.iot_rule_t3.arn
}

# IoT Rule for Topic T4
resource "aws_iot_topic_rule" "iot_rule_t4" {
  name        = "iot_to_lambda_t4"
  enabled     = true
  sql         = "SELECT * FROM 'T4'"
  sql_version = "2016-03-23"

  lambda {
    function_arn = aws_lambda_function.iot_handler.arn
  }
}


resource "aws_lambda_permission" "allow_iot_t4" {
  statement_id  = "AllowExecutionFromIoTT4"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.iot_handler.function_name
  principal     = "iot.amazonaws.com"
  source_arn    = aws_iot_topic_rule.iot_rule_t4.arn
}

# IoT Rule for Topic T5
resource "aws_iot_topic_rule" "iot_rule_t5" {
  name        = "iot_to_lambda_t5"
  enabled     = true
  sql         = "SELECT * FROM 'T5'"
  sql_version = "2016-03-23"

  lambda {
    function_arn = aws_lambda_function.iot_handler.arn
  }
}

resource "aws_lambda_permission" "allow_iot_t5" {
  statement_id  = "AllowExecutionFromIoTT5"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.iot_handler.function_name
  principal     = "iot.amazonaws.com"
  source_arn    = aws_iot_topic_rule.iot_rule_t5.arn
}

# IoT Rule for Topic T6

resource "aws_iot_topic_rule" "iot_rule_t6" {
  name        = "iot_to_lambda_t6"
  enabled     = true
  sql         = "SELECT * FROM 'T6'"
  sql_version = "2016-03-23"

  lambda {
    function_arn = aws_lambda_function.iot_handler.arn
  }
}


resource "aws_lambda_permission" "allow_iot_t6" {
  statement_id  = "AllowExecutionFromIoTT6"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.iot_handler.function_name
  principal     = "iot.amazonaws.com"
  source_arn    = aws_iot_topic_rule.iot_rule_t6.arn
}
# IoT Rule for Topic T7
resource "aws_iot_topic_rule" "iot_rule_t7" {
  name        = "iot_to_lambda_t7"
  enabled     = true
  sql         = "SELECT * FROM 'T7'"
  sql_version = "2016-03-23"

  lambda {
    function_arn = aws_lambda_function.iot_handler.arn
  }
}
resource "aws_lambda_permission" "allow_iot_t7" {
  statement_id  = "AllowExecutionFromIoTT7"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.iot_handler.function_name
  principal     = "iot.amazonaws.com"
  source_arn    = aws_iot_topic_rule.iot_rule_t7.arn
}

# IoT Rule for Topic T8
resource "aws_iot_topic_rule" "iot_rule_t8" {
  name        = "iot_to_lambda_t8"
  enabled     = true
  sql         = "SELECT * FROM 'T8'"
  sql_version = "2016-03-23"

  lambda {
    function_arn = aws_lambda_function.iot_handler.arn
  }
}
resource "aws_lambda_permission" "allow_iot_t8" {
  statement_id  = "AllowExecutionFromIoTT8"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.iot_handler.function_name
  principal     = "iot.amazonaws.com"
  source_arn    = aws_iot_topic_rule.iot_rule_t8.arn
}

