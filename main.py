import json
import speech_rec_hi as sr_hi
import speech_rec_eng as sr_eng
import translate as ts
import retranslate as rt
import pickle
import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential, Model, load_model
from englisttohindi.englisttohindi import EngtoHindi
import pyttsx3

engine = pyttsx3.init()  # object creation
# engine.setProperty("languages", "hi")
# voices = engine.getProperty('voices')
# for voice in voices:
#     print(f"Voice: {voice.name}")

# engine.setProperty("voice", voices[2].id)
# voices = engine.getProperty("voices")  # getting details of current voice


# Function to convert text to
# speech
def SpeakText(command):
    # Initialize the engine
    print(command)
    engine.say(command)
    engine.runAndWait()

classes = pickle.load(open("classes.pkl", "rb"))
tokenizer = pickle.load(open("tokenizer.pkl", "rb"))
label_encoder = pickle.load(open("label_encoder.pkl", "rb"))
model = load_model("Intent_Classification_ordered_split.h5")


class IntentClassifier:
    def __init__(self, classes, model, tokenizer, label_encoder):
        self.classes = classes
        self.classifier = model
        self.tokenizer = tokenizer
        self.label_encoder = label_encoder

    def get_intent(self, text):
        self.text = [text]
        self.test_keras = self.tokenizer.texts_to_sequences(self.text)
        self.test_keras_sequence = pad_sequences(
            self.test_keras, maxlen=maxLen, padding="post"
        )
        self.pred = self.classifier.predict(self.test_keras_sequence)
        return self.label_encoder.inverse_transform(np.argmax(self.pred, 1))[0]


answer = pd.read_csv("ZineNLP_Intent.csv")

prev_index = 0

ans = "n"
print("Please choose the language \n1.hindi \n2.english\n")
lang = int(input("Enter your choice : "))
# if lang == 1:
engine.setProperty("voice", "com.apple.speech.synthesis.voice.Kiyara")

while 1:
    ans = input("Do you want to ask a question y/n : ")
    if ans in "nN":
        break
    if lang == 1:
        que = sr_hi.speech_rec()
        que = json.loads(que)
        que = que["text"]
        print(que)
        que = ts.translate_hi_en(que)
    else:
        que = sr_eng.speech_rec()
        que = json.loads(que)
        que = que["text"]
        print(que)

    maxLen = 18
    nlu = IntentClassifier(classes, model, tokenizer, label_encoder)
    intent = nlu.get_intent(que)

    if intent == "Next":
        prev_cat = answer.iloc[prev_index, 0]
        if answer.iloc[prev_index + 1, 0] == prev_cat:
            prev_index += 1
            ans = answer.iloc[prev_index, 4]
        else:
            ans = "There is no sequence to the current question"

    elif intent == "Repeat":
        ans = ans
    else:
        ans = answer[answer["Intent"] == intent]
        prev_index = ans.index.to_numpy()[0]
        ans = ans.iloc[0, 4]

    # if lang == 1:
        # ans = rt.translate_en_hi(ans)
    ans=EngtoHindi(ans)
    ans=ans.convert

    SpeakText(ans)
