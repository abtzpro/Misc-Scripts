import requests
import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np

# function to record audio sample from microphone
def record_audio():
    duration = 5  # duration in seconds
    fs = 44100  # sample rate
    recording = sd.rec(duration * fs, samplerate=fs, channels=1)
    sd.wait()
    return fs, recording

# function to convert audio sample to WAV format
def convert_to_wav(fs, recording):
    filename = "audio_sample.wav"
    wav.write(filename, fs, recording)
    return filename

# function to send audio sample to online API for translation
def translate_audio(filename):
    url = "https://api.babylator.com/translate"
    files = {'file': open(filename, 'rb')}
    response = requests.post(url, files=files)
    return response.json()['translation']

# function to get user feedback on translation accuracy
def get_user_feedback(translation):
    feedback = input(f"Translation: {translation}. Was this translation accurate? (y/n) ")
    return feedback.lower() == 'y'

# main function to run the baby translator app
def run_baby_translator():
    # record audio sample
    fs, recording = record_audio()

    # convert audio sample to WAV format
    filename = convert_to_wav(fs, recording)

    # translate audio sample using online API
    translation = translate_audio(filename)

    # get user feedback on translation accuracy
    feedback = get_user_feedback(translation)

    # update translation accuracy rating on online API
    url = "https://api.babylator.com/rate_translation"
    data = {'translation': translation, 'accuracy': feedback}
    response = requests.post(url, data=data)

    return translation

if __name__ == '__main__':
    translation = run_baby_translator()
    print(f"Translation: {translation}")
