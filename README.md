- Python 3: https://www.python.org/
- Docker: https://www.docker.com/

Rename/copy config.template.py to config.py
Download whisper's models (https://github.com/openai/whisper#available-models-and-languages) and update `WHISPER_MODEL_PATH` in config.py with the path to the model file of your choice.
Register for a DeepL account on https://www.deepl.com/ and update `DEEPL_AUTH_KEY` in config.py with your key.
SET `SPEAKER_ID` in voicevox_client/voice_config.py to your desired speaker ID. See below for how to check the voices out.

```bash
# Always use a venv for these things
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

```bash
# Depends on whether you have GPU or not
# With GPU
docker compose -f docker-compose.gpu.yml up
# Without GPU
docker compose -f docker-compose.cpu.yml up
```

# Get list of Voicevox Speakers

Start python console with asyncio: `python -m asyncio`
Paste the code below:

```python
from voicevox_client.client import Client

async with Client() as client:
    for speaker in await client.fetch_speakers():
        print(speaker)
```

`speaker_uuid` from this can be used to get more info about the speaker.
Each speaker has a `styles` array, each element has its own `id` that can be used to for speaker initialization/voice synthesis.

We can combine `speaker_uuid` and `id` to check voice samples from the get speaker info API.

# Get a single Voicevox Speaker's info

Start python console with asyncio: `python -m asyncio`
Paste the code below:

```python
from voicevox_client.client import Client

async with Client() as client:
    speaker = await client.fetch_speaker_info("<speaker_uuid>")
    # speaker["portrait"] is an base64 encoded image
    # speaker["style_infos"] is an array where each element contains id (style id), portrait (base64 encoded image), icon (base64 encoded image), voice_samples (array of base64 encoded voice samples)
    # Sample code to write the base64 encoded data to a file:
    # decoded = base64.b64decode(speaker["style_infos"][0]["voice_samples"][0])
    # out_file = ("test.wav")
    # with open(out_file, 'wb') as file:
    #     file.write(decoded)
```

# Sample of using vox client alone to do TTS

Start python console with asyncio: `python -m asyncio`

```python
from voicevox_client.client import Client

async with Client() as client:
     with open("test.wav", "wb") as f:
        f.write(await client.text_to_speech("交流できて嬉しいです", speaker_id=10))
```
