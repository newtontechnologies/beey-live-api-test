# beey-live-api-test

Testing utilities for Beey live transcription API

## The `api-test.py` script

This script reads a WAV audio file and sends its contents to the WebSocket server in chunks to simulate real-time audio streaming.

### Prerequisites

- Python 3.10 or later (earlier versions may work, but have not been tested)
- The `websocket-client` library (version 1.6.1)

### Usage

```bash
python3 api-test.py <audio-file> <language>
```

Where:
- `<audio-file>` is the path to the WAV audio file to be transcribed
- `<language>` is the language code to use for transcription (e.g., `en-US` for English, `cs-CZ` for Czech)

### Audio file format

The API works best with PCM s16le WAV files with a sample rate of 16 kHz. Other WAV formats may work, but have not been tested.
