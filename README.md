# 🗣️ AWS Text-to-Speech Converter

This project demonstrates an AWS Lambda function that converts text to speech using AWS Polly. The Lambda function stores the resulting audio file in an S3 bucket, and the project is fully managed using Infrastructure as Code (IaC) with Terraform.

---

## 🗂 Project Structure

- `lambda_function.py`: Python code for the AWS Lambda function.
- `lambda_function.zip`: Zipped version of the Lambda code (required by Terraform).
- `main.tf`: Terraform configuration to provision all required AWS resources (Lambda, S3, IAM).
- `invoke_lambda.py`: Python script to trigger the Lambda function and pass user input.
- `terraform_outputs.json`: JSON file that stores dynamic output values (e.g., Lambda function name) from Terraform.

---

## ⚙️ Setup Instructions

### ✅ Prerequisites

- **AWS Account** with programmatic access (access key & secret key).
- **Terraform** installed. [Install Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)
- **Python 3.8+** and **Boto3** installed. [Install Python](https://www.python.org/downloads/)

---

### 🛠 Steps

#### 1. **Clone the Repository**

```bash
git clone https://github.com/JadEletry/aws-text-to-speech.git
cd aws-text-to-speech
```

#### 2. **Zip the Lambda Code**

Before deploying, zip the Lambda function code:

```bash
Compress-Archive -Path lambda_function.py -DestinationPath lambda_function.zip -Force
```

#### 3. **Initialize Terraform**

```bash
terraform init
```

#### 4. **Apply Terraform Configuration**

```bash
terraform apply
```

- Type `yes` when prompted.
- This provisions:
  - A secure S3 bucket
  - An AWS Lambda function
  - IAM roles and policies
  - Environment variables (e.g., bucket name)
  - Permissions for Polly and S3

#### 5. **Export Terraform Outputs**

After deploying, export the outputs to a JSON file:

```bash
terraform output -json > terraform_outputs.json
```

This file is used by the Python script to dynamically fetch the deployed Lambda function name.

---

### ▶️ 6. **Run the App**

```bash
python invoke_lambda.py
```

- Follow the prompts to:
  - Enter the text to convert
  - Select a language
  - Choose a voice
- The function will upload an MP3 file to the S3 bucket

Example output:
```
Text to Speech conversion successful! File saved as output_<uuid>.mp3
```

---

### 🧹 7. **Clean Up Resources**

To avoid ongoing AWS charges, run:

```bash
terraform destroy
```

Type `yes` to confirm when prompted.

---

## 📄 File Descriptions

### `lambda_function.py`

The Lambda function code. Uses AWS Polly to synthesize speech and uploads it to S3. The bucket name is injected from Terraform as an environment variable.

### `lambda_function.zip`

Zipped deployment package for the Lambda function. Terraform uses this to upload the code.

### `main.tf`

Defines all AWS infrastructure:
- S3 bucket with encryption
- Lambda function with IAM role
- Polly + S3 permissions
- Environment variables
- Terraform outputs

### `invoke_lambda.py`

CLI app to:
- Take user input
- Dynamically load the Lambda function name
- Call the Lambda function using Boto3
- Display the response and audio filename

---

## 💡 Notes

- You can check the uploaded MP3s in the AWS Console → S3 bucket
- To expose the files publicly or generate pre-signed download links, modify the S3 bucket policy or use `s3.generate_presigned_url()`
