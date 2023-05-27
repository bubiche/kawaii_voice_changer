# Kawaii Voice Changer

What if you can fulfill your dream of becoming a cute girl? Well, it's possible now (sort of).

- Audio transcription is done with [Whisper](https://github.com/openai/whisper).
- Translation is done with [DeepL](https://www.deepl.com/).
- Text to (cute) speech is done with [Voicevox](https://github.com/VOICEVOX/voicevox_engine).

## Table of Contents
* [Demo](#demo)
* [Setup](#setup)
* [Quickstart](#quickstart)
* [Possible Improvement](#possible-improvement)
* [Helpful things](#helpful-things)
  + [Get list of Voicevox Speakers](#get-list-of-voicevox-speakers)
  + [Get a single Voicevox Speaker info](#get-a-single-voicevox-speaker-info)
  + [Sample of using vox client alone to do TTS](#sample-of-using-vox-client-alone-to-do-tts)
  + [List audio devices](#list-audio-devices)
  + [Use audio output for voice chat](#use-audio-output-for-voice-chat)

## Demo 

On my laptop, only CPU

https://github.com/bubiche/kawaii_voice_changer/assets/15794264/1889f292-95bb-488d-9ed0-9291062e9f4b

## Setup

- Install [Docker](https://www.docker.com) for voicevox engine
- Install Python 3.10 + [Poetry](https://python-poetry.org/), I recommend using [asdf](https://asdf-vm.com/) for this.
- Install dependencies with Poetry by running `poetry install`. If you don't want to use it, check `pyproject.toml` for Python and package versions.
- Rename/copy `config.template.py` to `config.py`.
- Download whisper's models (https://github.com/openai/whisper#available-models-and-languages) and update `WHISPER_MODEL_PATH` in config.py with the path to the model file of your choice.
- Update the array `VOICE_OUTPUT_DEVICE_IDS` in config.py with devices that you want the final voice to go to (e.g. speaker/headphone/"fake" microphone for voice chats)
- SET `SPEAKER_ID` in voicevox_client/voice_config.py to your desired speaker ID. See below for how to check the voices out.

## Quickstart

Start Voicevox engine in 1 console:

```bash
# Depends on whether you have GPU or not
# With GPU
docker compose -f docker-compose.gpu.yml up
# Without GPU
docker compose -f docker-compose.cpu.yml up
```

Start the program in another console:

```bash
poetry run python main.py

# Or wish a shell inside poetry's virtualenv
poetry shell
python main.py
```

## Possible Improvement

- Move whisper audio transcription + voicevox engine to some cloud server with GPU or just [Google Colab](https://colab.research.google.com/) if internet connection is good so less local resource is needed and things will run faster.

## Helpful things

### Get list of Voicevox Speakers

Run this inside a python console with asyncio (`python -m asyncio`):

```python
from voicevox_client.client import Client

with Client() as client:
    for speaker in client.fetch_speakers():
        print(speaker)
```

`speaker_uuid` from this can be used to get more info about the speaker.
Each speaker has a `styles` array, each element has its own `id` that can be used to for speaker initialization/voice synthesis.

We can combine `speaker_uuid` and `id` to check voice samples from the get speaker info API.

### Get a single Voicevox Speaker info

Run this inside a python console with asyncio (`python -m asyncio`):

```python
from voicevox_client.client import Client

with Client() as client:
    speaker = client.fetch_speaker_info("<speaker_uuid>")
    # speaker["portrait"] is an base64 encoded image
    # speaker["style_infos"] is an array where each element contains id (style id), portrait (base64 encoded image), icon (base64 encoded image), voice_samples (array of base64 encoded voice samples)
    # Sample code to write the base64 encoded data to a file:
    # decoded = base64.b64decode(speaker["style_infos"][0]["voice_samples"][0])
    # out_file = ("test.wav")
    # with open(out_file, 'wb') as file:
    #     file.write(decoded)
```

### Sample of using vox client alone to do TTS

Run this inside a python console with asyncio (`python -m asyncio`):

```python
from voicevox_client.client import Client

with Client() as client:
     with open("test.wav", "wb") as f:
        f.write(client.text_to_speech("交流できて嬉しいです", speaker_id=10))
```

### List audio devices

Run this inside a python console:

```python
import sounddevice as sd

print(sd.query_devices())
```

### Use audio output for voice chat

Use something like [VB-CABLE](https://vb-audio.com/Cable/index.htm) to forward the audio output of this program to a fake audio input device, then use that fake the device as audio input for your voice chat application, should work with most games/Discord/Zoom.
