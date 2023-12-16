# import urllib.request

# urllib.request.urlretrieve(
#     "https://argosopentech.nyc3.digitaloceanspaces.com/argospm/translate-hi_en-1_1.argosmodel",
#     "translate-en_hi-1_1.argosmodel",
# )

from argostranslate import package
from argostranslate import translate


package.install_from_path("translate-en_hi-1_1.argosmodel")


def get_argos_model(source, target):
    lang = f"{source} -> {target}"
    source_lang = [
        model
        for model in translate.get_installed_languages()
        if lang in map(repr, model.translations_from)
    ]

    target_lang = [
        model
        for model in translate.get_installed_languages()
        if lang in map(repr, model.translations_to)
    ]

    return source_lang[0].get_translation(target_lang[0])


def translate_en_hi(text):
    argos_hi_en = get_argos_model("English", "Hindi")
    translated = argos_hi_en.translate(text)
    return translated
