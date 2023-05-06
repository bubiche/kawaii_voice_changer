import pathlib
import threading
import toggle
import config
import time
from voicevox_client.client import Client
import voicevox_client.voice_config as vc
import sounddevice as sd
import soundfile as sf


AUDIO_FILE_PATH = f"{pathlib.Path().resolve()}/audio_out.wav"

def speak_text(japanese_text_queue):
    """
    Get text from japanese_text_queue and output to audio devices configured with config.VOICE_OUTPUT_DEVICE_IDS

    Args:
        japanese_text_queue (queue.Queue): The queue to read translated Japanese texts from
    """
    with Client() as client:
        client.initialize_speaker(vc.SPEAKER_ID)

        print("VOICE VOX INITIALIZED")
        while True:
            if toggle.is_recording:
                time.sleep(0.5)
            else:
                text = japanese_text_queue.get()
                with open(AUDIO_FILE_PATH, "wb") as f:
                    f.write(client.text_to_speech(text, speaker_id=vc.SPEAKER_ID))
                    play_voice_threads = [threading.Thread(target=play_voice, args=(device_id,)) for device_id in config.VOICE_OUTPUT_DEVICE_IDS]
                    [t.start() for t in play_voice_threads]
                    [t.join() for t in play_voice_threads]

def play_voice(device_id):
    """
    Play audio to device specified by device_id
    """
    print(f"PLAYING ON DEVICE ID: {device_id}")
    data, sample_rate = sf.read(AUDIO_FILE_PATH, dtype='float32')

    sd.play(data, sample_rate, device=device_id, blocksize=1024)
    sd.wait()

# Alternative way using pyaudio
# def play_voice(device_id):
#     """
#     Play audio to device specified by device_id
#     """
#     with wave.open(AUDIO_FILE_PATH, 'rb') as wav_file:
#         p = pyaudio.PyAudio()
#         stream = p.open(format=p.get_format_from_width(wav_file.getsampwidth()),
#                         channels=wav_file.getnchannels(),
#                         rate=wav_file.getframerate(),
#                         output_device_index=device_id,
#                         output=True)

#         data = wav_file.readframes(wav_file.getnframes())

#         while data:
#             stream.write(data)
#             # 1024 is the magic number for chunk size
#             data = wav_file.readframes(1024)

#         stream.stop_stream()
#         stream.close()

#         p.terminate()
