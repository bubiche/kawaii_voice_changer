- Python 3: https://www.python.org/
- Docker: https://www.docker.com/

Rename/copy config.template.py to config.py
Download whisper's models (https://github.com/openai/whisper#available-models-and-languages) and update WHISPER_MODEL_PATH in config.py with the path to the model file of your choice.
Register for a DeepL account on https://www.deepl.com/ and update DEEPL_AUTH_KEY in config.py with your key.

```bash
# Always use a venv for these things
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```