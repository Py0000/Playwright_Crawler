from googletrans import Translator

def check_word_in_text(word, text):
    # Create a translator object
    translator = Translator()
    
    # Detect the language of the text
    lang = translator.detect(text).lang
    print(lang == "en")
    
    # Translate the word to the detected language
    translated_word = translator.translate(word, dest=lang).text
    print(translated_word)
    
    # Check if the translated word is in the text
    return translated_word in text


text = "Web"
actual = "Web Deleted"


print(check_word_in_text(text.lower(), actual.lower()))