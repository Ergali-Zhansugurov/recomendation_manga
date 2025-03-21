from deep_translator import GoogleTranslator

def translate_text(text: str, target: str = "en") -> str:
    try:
        translated = GoogleTranslator(source='auto', target=target).translate(text)
        return translated
    except Exception as e:
        # Если перевод не удался, возвращаем исходный текст
        return text