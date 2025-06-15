resource "aws_lambda_function" "warm_feast" {
  function_name = "warm_feast_store"
  runtime       = "python3.10"
  handler       = "cleanup.lambda_handler"
  filename      = "feature_store/cleanup.zip"
  timeout       = 10
}

resource "aws_cloudwatch_event_rule" "every_5min" {
  schedule_expression = "rate(5 minutes)"
}

resource "aws_cloudwatch_event_target" "warm_target" {
  rule      = aws_cloudwatch_event_rule.every_5min.name
  target_id = "lambda"
  arn       = aws_lambda_function.warm_feast.arn
}
