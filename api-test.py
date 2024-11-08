import sys
import json
import struct
import wave
import time
import websocket
import threading
import ssl

# WebSocket server URL
SERVER_URL = "wss://stage.beey.io"

# API token for the WebSocket server
API_TOKEN = "xxxx"

# Frame rate of the audio file
SAMPLE_RATE = 16000

# Bytes per sample
BYTES_PER_SAMPLE = 2

# Number of frames per chunk
SAMPLES_PER_CHUNK = 8192

# Size of each chunk in bytes
CHUNK_SIZE = SAMPLES_PER_CHUNK * BYTES_PER_SAMPLE

# Chunk delay
DELAY = SAMPLES_PER_CHUNK / SAMPLE_RATE

def create_wav_header():
    header = "RIFF".encode() # RIFF header
    header += struct.pack('<I', 0xFFFFFFFF) # file size
    header += 'WAVEfmt '.encode() # WAVE header
    header += struct.pack('<I', 16) # size of fmt chunk
    header += struct.pack('<H', 1) # audio format (PCM)
    header += struct.pack('<H', 1) # number of channels
    header += struct.pack('<I', SAMPLE_RATE) # sample rate
    header += struct.pack('<I', SAMPLE_RATE * BYTES_PER_SAMPLE) # byte rate
    header += struct.pack('<H', BYTES_PER_SAMPLE) # block align
    header += struct.pack('<H', BYTES_PER_SAMPLE * 8) # bits per sample
    header += "data".encode() # data header
    header += struct.pack('<I', 0xFFFFFFFF) # size of data chunk
    return header

def send_audio_chunks(file_path, language):
    def on_open(ws):
        # Start a new thread for sending audio chunks to avoid blocking the WebSocket event loop
        send_thread = threading.Thread(target=send_audio_chunks, args=(ws, file_path))
        send_thread.start()

    def on_message(ws, message):
        print(f"Received message from server: {message}")

    def on_error(ws, error):
        print(f"Error: {error}")

    def on_close(ws, close_status_code, close_msg):
        print("Connection closed", close_status_code, close_msg)

    def send_audio_chunks(ws, file_path):
        ws.send(json.dumps({"ChunkSize": CHUNK_SIZE}))
        ws.send(create_wav_header(), opcode=websocket.ABNF.OPCODE_BINARY)
        
        # Open the WAV file
        with wave.open(file_path, 'rb') as wav_file:
            # Start reading and sending chunks
            while True:
                chunk = wav_file.readframes(SAMPLES_PER_CHUNK)
                if not chunk:
                    print("Finished streaming the audio file.")
                    break
                ws.send(chunk, opcode=websocket.ABNF.OPCODE_BINARY)

                # Wait for the duration of the chunk to simulate real-time streaming
                time.sleep(DELAY)
                
                print(f"Sent chunk of size {len(chunk)} bytes")

    uri = f"{SERVER_URL}/ws/LiveTranscription?language={language}&profile=subtitles"
    ws = websocket.WebSocketApp(
        uri,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        header={"Authorization:" + API_TOKEN}
    )

    # Run the WebSocket client (listens for messages)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    ws.close()
    print("Connection closed")

# Get the file path and language from the command line arguments    
if len(sys.argv) < 3:
    print("Usage: python3 api-test.py <file_path> <language>")
    sys.exit(1)

file_path = sys.argv[1]
language = sys.argv[2]

print(f"Sending audio chunks from {file_path} in {language} language")

send_audio_chunks(file_path, language)
