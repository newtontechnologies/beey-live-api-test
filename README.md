# Beey Live API Testing Utility

Testing utilities for Beey live transcription API

The `api-test.py` is a Python script that reads an audio stream from STDIN and sends its contents to the WebSocket server in chunks.

## Prerequisites

- ffmpeg (for producing the audio stream)
- Python 3.10 or later (earlier versions may work, but have not been tested)
- The `python-dotenv` library
- The `websocket-client` library (version 1.6.1)

## Setup

1. After installing ffmpeg and Python, install the required Python libraries by running the following command:
   ```bash
   python3.10 -m pip install websocket-client==1.6.1 python-dotenv
   ```
2. Rename the `.env.example` file to `.env` and fill in the AUTH_TOKEN with your API key.

## Transcribing a WAV audio file

To transcribe a WAV audio file in, run the script with the following command:

```bash
ffmpeg -i <your-file.wav> -f wav pipe:1 | python3 api-test.py <language>
```

Where:
- `<your-file.wav>` is the path to the WAV audio file to be transcribed
- `<language>` is the language code to use for transcription (e.g., `en-US` for English, `cs-CZ` for Czech)

The API works best with PCM s16le WAV files with a sample rate of 16 kHz. Other WAV formats will probably work too.

## Transcribing an AAC live audio stream

To transcribe a live stream with AAC audio, run the script with the following command:

```bash
ffmpeg -i <stream-url> -map 0:1 -f adts pipe:1 | python3 api-test.py <language>
```

Where:
- `<stream-url>` is the URL of the live stream to be transcribed
- `<language>` is the language code to use for transcription (e.g., `en-US` for English, `cs-CZ` for Czech)

## Supported languages

The API supports the following languages for live test transcriptions:

- Czech (cs-CZ)
- English (en-US)
