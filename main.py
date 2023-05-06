import queue
import threading
import time
import record_audio as ra
import transcribe_audio as ta
import translate_text as tt
import speak_text as st
import toggle
from pynput import keyboard

def on_key_press(key):
    if key == keyboard.Key.space:
        toggle.is_recording = not toggle.is_recording
        print(f"is_recording: {toggle.is_recording}")


def is_any_thread_alive(threads):
    return True in [t.is_alive() for t in threads]

if __name__ == "__main__":
    audio_queue = queue.Queue()
    english_text_queue = queue.Queue()
    japanese_text_queue = queue.Queue()

    record_audio_thread = threading.Thread(target=ra.record_audio, args=(audio_queue,), daemon=True)
    transcribe_audio_thread = threading.Thread(target=ta.transcribe_audio, args=(audio_queue, english_text_queue), daemon=True)
    translate_text_thread = threading.Thread(target=tt.translate_text, args=(english_text_queue, japanese_text_queue), daemon=True)
    speak_text_thread = threading.Thread(target=st.speak_text, args=(japanese_text_queue,), daemon=True)

    record_audio_thread.start()
    transcribe_audio_thread.start()
    translate_text_thread.start()
    speak_text_thread.start()

    listener = keyboard.Listener(on_press=on_key_press)
    listener.start()

    print("Press space to start/stop recording")

    while is_any_thread_alive([record_audio_thread, transcribe_audio_thread, translate_text_thread, speak_text_thread]):
        time.sleep(0)
