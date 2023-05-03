import speech_recognition as sr
import numpy as np
import torch
import toggle
import time

def record_audio(audio_queue, energy_threshold=300, pause_threshold=0.8, dynamic_energy_threshold=True):
    """
    Record audio and put it into audio_queue

    Args:
        audio_queue (queue.Queue): The queue to put the recorded audio in to be processed by transcribe_audio
        energy_threshold (integer): Energy level for microphone to detect (default is 300)
        pause_threshold (float): Pause time before currently recorded audio ends (default is 0.8)
        dynamic_energy_threshold (boolean): Toggle dynamic energy for the recognizer
    """

    r = sr.Recognizer()
    r.energy_threshold = energy_threshold
    r.pause_threshold = pause_threshold
    r.dynamic_energy_threshold = dynamic_energy_threshold

    with sr.Microphone(sample_rate=16000) as source:
        r.adjust_for_ambient_noise(source)

        is_first_time_after_toggling_record = True
        while True:
            if toggle.is_recording:
                if is_first_time_after_toggling_record:
                    print("Audio Record Ready")
                    is_first_time_after_toggling_record = False
                audio = r.listen(source)
                torch_audio = torch.from_numpy(np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0)
                audio_data = torch_audio
                audio_queue.put_nowait(audio_data)
            else:
                is_first_time_after_toggling_record = True
                time.sleep(0.5)
