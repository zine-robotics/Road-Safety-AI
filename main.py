# import urllib.request

# urllib.request.urlretrieve(
#     "https://argosopentech.nyc3.digitaloceanspaces.com/argospm/translate-hi_en-1_1.argosmodel",
#     "translate-hi_en-1_1.argosmodel",
# )

import speech_rec as sr
from argostranslate import package
from argostranslate import translate
import json

package.install_from_path("translate-hi_en-1_1.argosmodel")

que = sr.speech_rec()
print(que)
que = json.loads(que)
print(que["text"])


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


argos_hi_en = get_argos_model("Hindi", "English")

translated = argos_hi_en.translate(que["text"])

print(translated)
