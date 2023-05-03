import config
import deepl

def translate_text(english_text_queue, japanese_text_queue):
    text_translator = deepl.Translator(config.DEEPL_AUTH_KEY)

    print("Translate Text Ready")

    while True:
        transcribed_text = english_text_queue.get()
        print(f"ENGLISH: {transcribed_text}")
        translated_text = text_translator.translate_text(transcribed_text, target_lang="JA")
        print(f"JAPANESE: {translated_text}")
        # japanese_text_queue.put_nowait(translated_text)