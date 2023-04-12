import os
import openai
from dotenv import load_dotenv
import pyttsx3
import boto3
import sounddevice as sd
from scipy.io.wavfile import write
import datetime
import urllib
import json
import time as tm

# Load and get environment variables
load_dotenv()
## OpenAI environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
model_engine = os.getenv("MODEL_ENGINE")
max_tokens = int(os.getenv("MAX_TOKENS"))
## Speech-to-text environment variables
sampling_frequency = int(os.getenv("SAMPLING_FREQUENCY"))
channels = int(os.getenv("CHANNELS"))
## AWS environment variables
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
s3_bucket_name = os.getenv("S3_BUCKET_NAME")
region_name = os.getenv("REGION_NAME")
## Text-to-speech environment variables
voice_rate = os.getenv("VOICE_RATE")

# Record audio
recording = sd.rec(int(5 * sampling_frequency), samplerate=sampling_frequency, channels=channels)
sd.wait()
# Save the recorded audio
time = datetime.datetime.now().strftime("%m-%d-%Y %H-%M-%S")
write(f"{time}.wav", sampling_frequency, recording)

# Upload audio to S3
s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
with open(f"{time}.wav", "rb") as f:
    s3_client.upload_fileobj(f, s3_bucket_name, f"{time}.wav")

# Create a client for AWS Transcribe
transcribe_client = boto3.client('transcribe', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)
# Use the client to create a transcription job
transcription_job_name = datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
response = transcribe_client.start_transcription_job(
    TranscriptionJobName=f'{transcription_job_name}',
    Media={'MediaFileUri': f's3://{s3_bucket_name}/{time}.wav'},
    MediaFormat='wav',
    LanguageCode='en-US'
)
# Wait for the job to finish
while True:
    status = transcribe_client.get_transcription_job(TranscriptionJobName=f'{transcription_job_name}')['TranscriptionJob']['TranscriptionJobStatus']
    if status in ['COMPLETED', 'FAILED']:
        break
    print("Job still in progress...")
    tm.sleep(3)
# Get the transcription results
if status == 'COMPLETED':
    response = transcribe_client.get_transcription_job(TranscriptionJobName=f'{transcription_job_name}')
    transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
    transcript_response = urllib.request.urlopen(transcript_uri)
    transcript_data = transcript_response.read()
    transcript_text = json.loads(transcript_data)['results']['transcripts'][0]['transcript']

# Get response from OpenAI
response = openai.ChatCompletion.create(
    model=model_engine,
    messages=[{"content": transcript_text, "role": "user"}],
    max_tokens=max_tokens,
)
message = response.choices[0].message.content

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', voice_rate)
engine.setProperty('voices', engine.getProperty('voices')[0].id)

# Print and speak response
print(message)
engine.say(message)
engine.runAndWait()