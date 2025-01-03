import sys
import os
import json
import websocket
import threading
import ssl
from dotenv import load_dotenv

load_dotenv()

# WebSocket server URL
SERVER_URL = os.getenv("SERVER_URL")

# API token for the WebSocket server
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

# Size of each chunk in bytes
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE"))

def start_transcription(language):
    def on_open(ws):
        # Start a new thread for sending audio chunks to avoid blocking the WebSocket event loop
        send_thread = threading.Thread(target=send_audio_chunks, args=(ws,))
        send_thread.start()

    def on_message(ws, message):
        print(f"Received message from server: {message}")

    def on_error(ws, error):
        print(f"Error: {error}")

    def on_close(ws, close_status_code, close_msg):
        print("Connection closed", close_status_code, close_msg)

    def send_audio_chunks(ws):
        ws.send(json.dumps({"ChunkSize": CHUNK_SIZE}))
        while True:
            chunk = sys.stdin.buffer.read(CHUNK_SIZE)
            if not chunk:
                print("Finished streaming the audio file.")
                break
            ws.send(chunk, opcode=websocket.ABNF.OPCODE_BINARY)
                
            print(f"Sent chunk of size {len(chunk)} bytes")

    uri = f"{SERVER_URL}/ws/LiveTranscription?language={language}&profile=subtitles"
    ws = websocket.WebSocketApp(
        uri,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        header={"Authorization:" + AUTH_TOKEN}
    )

    # Run the WebSocket client (listens for messages)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    ws.close()
    print("Connection closed")

# Get the language from the command line arguments    
if len(sys.argv) < 2:
    print("Usage: <audio-stream> | python api-test.py <language>")
    sys.exit(1)

language = sys.argv[1]

print(f"Processing audio in {language} language")

start_transcription(language)
