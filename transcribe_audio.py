import whisper
import config
import torch

def transcribe_audio(audio_queue, english_text_queue):
    """
    Take audios from audio_queue and transcribe them into texts

    Args:
        audio_queue (queue.Queue): The queue to read from and transcribe
        english_text_queue (queue.Queue): The queue to put transcribe texts into
    """
    audio_model = whisper.load_model(config.WHISPER_MODEL_PATH).to("cuda" if torch.cuda.is_available() else "cpu")

    print('Audio Transcribe Ready')

    while True:
        audio_data = audio_queue.get()
        result = audio_model.transcribe(audio_data, fp16=False, language='english')
        english_text_queue.put_nowait(result["text"])
