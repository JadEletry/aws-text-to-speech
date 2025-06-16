provider "aws" {
  region = "ca-central-1"
}

resource "random_id" "bucket_id" {
  byte_length = 8
}

resource "aws_s3_bucket" "tts_bucket" {
  bucket = "my-bucket-output-${random_id.bucket_id.hex}"
  force_destroy = true

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

resource "aws_s3_bucket_policy" "tts_bucket_policy" {
  bucket = aws_s3_bucket.tts_bucket.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          AWS = aws_iam_role.lambda_role.arn
        },
        Action = [
          "s3:PutObject"
        ],
        Resource = "${aws_s3_bucket.tts_bucket.arn}/*"
      }
    ]
  })
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "polly_policy_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonPollyFullAccess"
}

resource "aws_iam_role_policy_attachment" "s3_policy_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_lambda_function" "tts_lambda" {
  filename         = "lambda_function.zip"
  function_name    = "TextToSpeechFunction-${random_id.bucket_id.hex}"  # Use a unique name
  role             = aws_iam_role.lambda_role.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.8"
  source_code_hash = filebase64sha256("lambda_function.zip")

  timeout = 15

  environment {
    variables = {
      BUCKET_NAME = aws_s3_bucket.tts_bucket.bucket
    }
  }

}

resource "aws_lambda_permission" "allow_invoke" {
  statement_id  = "AllowExecutionFromInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.tts_lambda.function_name
  principal     = "lambda.amazonaws.com"
}

output "lambda_function_name" {
  value = aws_lambda_function.tts_lambda.function_name
}


