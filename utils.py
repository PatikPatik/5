from gettext import translation

def get_translator(lang_code: str):
    return translation(
        'messages', localedir='locales', languages=[lang_code], fallback=True
    ).gettext
