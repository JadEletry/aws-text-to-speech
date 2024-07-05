# AWS Text-to-Speech Converter

This project demonstrates an AWS Lambda function that converts text to speech using AWS Polly. The project is managed using Infrastructure as Code (IaC) with Terraform.

## Project Structure

- `lambda_function.py`: Python code for the Lambda function.
- `lambda_function.zip`: Zipped Lambda function code.
- `main.tf`: Terraform configuration file for setting up AWS resources.
- `invoke_lambda.py`: Python script to invoke the Lambda function.

## Setup Instructions

### Prerequisites

- **AWS Account**: You need an AWS account with the necessary permissions.
- **Terraform**: Installed on your local machine. [Terraform Installation Guide](https://learn.hashicorp.com/tutorials/terraform/install-cli)
- **Python and Boto3**: Installed on your local machine. [Python Installation Guide](https://www.python.org/downloads/)

### Steps

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/JadEletry/aws-text-to-speech.git
    cd aws-text-to-speech
    ```

2. **Initialize Terraform**:
    ```sh
    terraform init
    ```

3. **Apply Terraform Configuration**:
    ```sh
    terraform apply
    ```
   - Confirm the plan by typing `yes` when prompted.

4. **Invoke Lambda Function**:
    - Use the `invoke_lambda.py` script to test the function.

    ```sh
    python invoke_lambda.py
    ```

    - Follow the prompts to enter the text, select a language, and choose a voice.

5. **Clean Up**:
    - Delete the resources using Terraform when done to avoid charges:

    ```sh
    terraform destroy
    ```
    - Confirm the destruction by typing `yes` when prompted.

## Detailed Explanation

### lambda_function.py

This is the Python code for the Lambda function that uses AWS Polly to convert text to speech and stores the resulting audio file in an S3 bucket.

### lambda_function.zip

The Lambda function code must be zipped before being uploaded to AWS Lambda. This file contains the zipped version of `lambda_function.py`.

### main.tf

This is the Terraform configuration file that defines the AWS resources used in this project, including the S3 bucket, IAM roles, and the Lambda function.

### invoke_lambda.py

This Python script is used to invoke the Lambda function. It takes user input for text, language, and voice, and calls the Lambda function to perform the text-to-speech conversion.
