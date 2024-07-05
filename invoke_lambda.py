import boto3
import json

languages_and_voices = {
    'en-US': ['Joanna', 'Matthew', 'Ivy', 'Justin', 'Kendra', 'Kimberly', 'Salli', 'Joey'],
    'en-GB': ['Amy', 'Emma', 'Brian'],
    'es-ES': ['Miguel', 'Penelope', 'Lucia'],
    'fr-FR': ['Celine', 'Lea', 'Mathieu'],
    'de-DE': ['Hans', 'Marlene', 'Vicki'],
    # Add more languages and voices as needed
}

def display_languages_and_voices():
    print("Available languages and voices:\n")
    for language, voices in languages_and_voices.items():
        print(f"{language}: {', '.join(voices)}")

def invoke_lambda(text, language_code, voice_id):
    client = boto3.client('lambda', region_name='ca-central-1')  # Specify the correct region corresponding to your AWS console
    response = client.invoke(
        FunctionName='TextToSpeechFunction-d8757c2916ea5dc0',  # Ensure this matches your Lambda function name exactly
        InvocationType='RequestResponse',
        Payload=json.dumps({
            'text': text,
            'language_code': language_code,
            'voice_id': voice_id
        })
    )
    response_payload = json.loads(response['Payload'].read())
    
    print("Full response payload:")
    print(json.dumps(response_payload, indent=4))
    
    # Check if 'body' key exists in the response payload
    if 'body' in response_payload:
        print(response_payload['body'])
    else:
        print("Error: 'body' key not found in the response payload")

if __name__ == "__main__":
    display_languages_and_voices()
    text = input("\nEnter text: ")
    
    print("\nChoose a language code from the following:")
    for index, language in enumerate(languages_and_voices.keys(), start=1):
        print(f"{index}. {language}")

    language_choice = int(input("\nEnter the number corresponding to your chosen language: ")) - 1
    language_code = list(languages_and_voices.keys())[language_choice]
    
    print("\nChoose a voice from the following:")
    for index, voice in enumerate(languages_and_voices[language_code], start=1):
        print(f"{index}. {voice}")

    voice_choice = int(input("\nEnter the number corresponding to your chosen voice: ")) - 1
    voice_id = languages_and_voices[language_code][voice_choice]
    
    invoke_lambda(text, language_code, voice_id)
