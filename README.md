# Voice-To-GPT

My attempt at creating a personal voice assistant using GPT. When the system is offline, it uses [GPT4All](https://github.com/nomic-ai/gpt4all), and when it's online it uses [ChatGPT](https://chat.openai.com/).

## Usage
1. Install libraries with `pip install -r requirements.txt`
2. Upgrade your [OpenAI account](https://openai.com/pricing) and [create an API key](https://platform.openai.com/docs/api-reference/authentication)
3. Create an AWS account, create a new user, give it the `AmazonS3FullAccess` and `AmazonTranscribeFullAccess` permissions, and create an API key for the user
4. Create a `.env` file and add all the following environment variables
5. Run the script with `python main.py`

## Environment Variables (.env)
- OPENAI_API_KEY
- MODEL_ENGINE
- VOICE_RATE
- MAX_TOKENS
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- S3_BUCKET_NAME
- REGION_NAME
- SAMPLING_FREQUENCY
- CHANNELS

## Resources
- [GPT4All](https://github.com/nomic-ai/gpt4all)
- [ChatGPT](https://chat.openai.com/)
- [Integrate ChatGPT with Voice to Text](https://betterprogramming.pub/how-to-integrate-chatgpt-with-voice-to-text-with-python-40300b8a77d1)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)