import boto3

with open('speech.txt', 'r') as file:
    text = file.read()
    print(text)


polly = boto3.client('polly')


response = polly.synthesize_speech(
    Engine='generative',
    Outputformat='mp3',
    Text=text,
    VoiceId='Stephen'
)


audioStream = response['AudioStream']


with open("example.mp3","wb") as f:
    f.write(audioStream.read())
    print("Polly output saved.")
