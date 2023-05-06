import config
import deepl

def translate_text(english_text_queue, japanese_text_queue):
    """
    Read English text from english_text_queue, translate to Japanese and put into japanese_text_queue
    Args:
        english_text_queue (queue.Queue): The queue of transcribed English texts
        japanese_text_queue (queue.Queue): The queue to put translated Japanese texts into
    """
    text_translator = deepl.Translator(config.DEEPL_AUTH_KEY)

    print("Translate Text Ready")

    while True:
        transcribed_text = english_text_queue.get()
        print(f"ENGLISH: {transcribed_text}")
        translated_text = text_translator.translate_text(transcribed_text, target_lang="JA")
        print(f"JAPANESE: {translated_text}")
        japanese_text_queue.put_nowait(translated_text)
