
"""
Piper TTS Script for NomadPuddy

This script uses Piper for text-to-speech conversion.

IMPORTANT: Piper voice models should be placed in the ~/piper_models directory.
Each voice requires two files: a .onnx file and a .onnx.json file.
Download these from: https://huggingface.co/rhasspy/piper-voices/tree/main/en/en_US

For example, for the 'lessac' voice, you need:
~/piper_models/en_US-lessac-medium.onnx
~/piper_models/en_US-lessac-medium.onnx.json
"""

# Alternate info: Download any voices you want from Piper TTS Github page. Place both the config file and the voice...
#in a directory of your choice and modify the path below as needed.
PIPER_VOICES = {
    "amy": {
        "model": "/home/scott/piper_models/en_US-amy-medium.onnx",
        "config": "/home/scott/piper_models/en_en_US_amy_medium_en_US-amy-medium.onnx.json"
    },
    "joe": {
        "model": "/home/scott/piper_models/en_US-joe-medium.onnx",
        "config": "/home/scott/piper_models/en_en_US_joe_medium_en_US-joe-medium.onnx.json"
    },
    "kathleen": {
        "model": "/home/scott/piper_models/en_US-kathleen-low.onnx",
        "config": "/home/scott/piper_models/en_en_US_kathleen_low_en_US-kathleen-low.onnx.json"
    },
    "kristin": {
        "model": "/home/scott/piper_models/en_US-kristin-medium.onnx",
        "config": "/home/scott/piper_models/en_en_US_kristin_medium_en_US-kristin-medium.onnx.json"
    },
    "lessac": {
        "model": "/home/scott/piper_models/en_US-lessac-medium.onnx",
        "config": "/home/scott/piper_models/en_en_US_lessac_medium_en_US-lessac-medium.onnx.json"
    },
    "libritts": {
        "model": "/home/scott/piper_models/en_US-libritts-high.onnx",
        "config": "/home/scott/piper_models/en_en_US_libritts_high_en_US-libritts-high.onnx.json"
    },
    "libritts_r": {
        "model": "/home/scott/piper_models/en_US-libritts_r-medium.onnx",
        "config": "/home/scott/piper_models/en_en_US_libritts_r_medium_en_US-libritts_r-medium.onnx.json"
    },
    "norman": {
        "model": "/home/scott/piper_models/en_US-norman-medium.onnx",
        "config": "/home/scott/piper_models/en_en_US_norman_medium_en_US-norman-medium.onnx.json"
    }
}
import paho.mqtt.client as mqtt
import subprocess
import re
import os
import time

MQTT_BROKER = "192.168.8.110"
MQTT_PORT = 1883
MQTT_TOPIC_OUTPUT = "llm/output"
MQTT_TOPIC_VOICE = "nomadpuddy/voice_selection"

# Speech settings
LENGTH_SCALE = 1  # 1.0 is normal speed, <1.0 is faster, >1.0 is slower
SENTENCES_PER_CHUNK = 4
PAUSE_BETWEEN_CHUNKS = 0.1


DEFAULT_VOICE = "lessac"
CURRENT_VOICE = DEFAULT_VOICE

print(f"Starting with default voice: {CURRENT_VOICE}")
print(f"Length scale (speech rate): {LENGTH_SCALE}")
print(f"Sentences per chunk: {SENTENCES_PER_CHUNK}")

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC_OUTPUT)
    client.subscribe(MQTT_TOPIC_VOICE)

def on_message(client, userdata, msg):
    global CURRENT_VOICE
    if msg.topic == MQTT_TOPIC_VOICE:
        new_voice = msg.payload.decode()
        if new_voice in PIPER_VOICES:
            CURRENT_VOICE = new_voice
            print(f"Voice changed to: {CURRENT_VOICE}")
    elif msg.topic == MQTT_TOPIC_OUTPUT:
        print(f"Received message: {msg.payload.decode()}")
        text_to_speech(msg.payload.decode())

def preprocess_text(text):
    # Remove special characters and extra whitespace
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    text = ' '.join(text.split())
    return text

def split_into_sentences(text):
    # Split the text into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return sentences

def group_sentences(sentences, group_size):
    return [' '.join(sentences[i:i+group_size]) for i in range(0, len(sentences), group_size)]

def text_to_speech(text):
    global CURRENT_VOICE
    text = preprocess_text(text)
    sentences = split_into_sentences(text)
    chunks = group_sentences(sentences, SENTENCES_PER_CHUNK)
    
    if CURRENT_VOICE not in PIPER_VOICES:
        print(f"Error: Voice '{CURRENT_VOICE}' not found in PIPER_VOICES")
        return

    voice_config = PIPER_VOICES[CURRENT_VOICE]
    if "model" not in voice_config or "config" not in voice_config:
        print(f"Error: Invalid configuration for voice '{CURRENT_VOICE}'")
        return

    for chunk in chunks:
        try:
            command = (f'echo "{chunk}" | piper '
                       f'--model {voice_config["model"]} '
                       f'--config {voice_config["config"]} '
                       f'--length-scale {LENGTH_SCALE} '
                       f'--output_raw | paplay --rate=22050 --channels=1 --format=s16le --raw')
            print(f"Executing command: {command}")  # Debug print
            subprocess.run(command, shell=True, check=True)
            time.sleep(PAUSE_BETWEEN_CHUNKS)
        except subprocess.CalledProcessError as e:
            print(f"Error in text-to-speech conversion: {e}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            print(f"Current voice: {CURRENT_VOICE}")
            print(f"Voice config: {voice_config}")
            
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)

try:
    print(f"Starting with default voice: {CURRENT_VOICE}")
    print(f"Speech rate: {LENGTH_SCALE}")
    print(f"Sentences per chunk: {SENTENCES_PER_CHUNK}")
    client.loop_forever()
except KeyboardInterrupt:
    print("Script terminated by user")
finally:
    client.disconnect()


