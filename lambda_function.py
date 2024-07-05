import json
import boto3
import uuid

def lambda_handler(event, context):
    text = event.get('text', 'Hello World!')
    language_code = event.get('language_code', 'en-US')
    voice_id = event.get('voice_id', 'Joanna')
    
    polly = boto3.client('polly')
    
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId=voice_id,
        LanguageCode=language_code
    )
    
    audio_stream = response['AudioStream'].read()
    
    s3 = boto3.client('s3')
    bucket_name = 'my-bucket-output'  # Replace with your unique S3 bucket name which the terraform script automatically created for you
    file_name = f'output_{uuid.uuid4()}.mp3'
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=audio_stream)
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Text to Speech conversion successful! File saved as {file_name}')
    }
