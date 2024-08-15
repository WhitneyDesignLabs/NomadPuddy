import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import paho.mqtt.client as mqtt
import threading
import time
import logging
import queue

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the Whisper model
model = whisper.load_model("tiny")
model = model.to("cpu")
model.eval()

# MQTT setup
mqtt_broker = "192.168.8.110" #Use the address of the Raspberry Pi or  the MQTT broker
mqtt_port = 1883
mqtt_topic = "stt/output"

client = mqtt.Client()
client.connect(mqtt_broker, mqtt_port, 60)
client.loop_start()

# Audio parameters
RATE = 16000
CHUNK = 1024
#Change this as needed. Higher number is less sensitive. We started at 0.01.
SILENCE_THRESHOLD = 0.02
SILENCE_DURATION = 1.5  # seconds of silence to stop recording

def audio_callback(indata, frames, time, status):
    if status:
        logging.warning(f"Audio callback status: {status}")
    audio_queue.put(indata.copy())

def vad(audio_chunk, threshold):
    return np.sqrt(np.mean(audio_chunk**2)) > threshold

def process_audio():
    buffer = []
    is_speaking = False
    silence_counter = 0
    
    with sd.InputStream(callback=audio_callback, channels=1, samplerate=RATE, blocksize=CHUNK):
        while True:
            audio_chunk = audio_queue.get().flatten()
            
            if vad(audio_chunk, SILENCE_THRESHOLD):
                if not is_speaking:
                    logging.info("Speech detected, starting to record...")
                is_speaking = True
                silence_counter = 0
                buffer.extend(audio_chunk)
            elif is_speaking:
                silence_counter += 1
                buffer.extend(audio_chunk)
                
                if silence_counter > int(SILENCE_DURATION * RATE / CHUNK):
                    is_speaking = False
                    logging.info("Silence detected, processing audio...")
                    audio_data = np.array(buffer, dtype=np.float32)
                    wav.write("temp_recording.wav", RATE, audio_data)
                    
                    result = model.transcribe("temp_recording.wav")
                    transcribed_text = result["text"].strip()
                    
                    if transcribed_text:
                        logging.info(f"Transcribed: {transcribed_text}")
                        client.publish(mqtt_topic, transcribed_text)
                    else:
                        logging.info("No speech detected in the audio.")
                    
                    buffer.clear()
            
            time.sleep(0.01)

def main():
    logging.info("Starting STT service...")
    global audio_queue
    audio_queue = queue.Queue()
    
    audio_thread = threading.Thread(target=process_audio)
    audio_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Stopping STT service...")
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()


