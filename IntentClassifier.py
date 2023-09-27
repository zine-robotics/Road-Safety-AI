import pickle
import json
import tensorflow as tf
import pandas as pd
import numpy as np
from tensorflow import keras
from tensorflow.keras.layers import (
    LSTM,
    Dense,
    Bidirectional,
    Dropout,
    Dense,
    Activation,
    Flatten,
    Embedding,
)
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential, Model, load_model
from tensorflow.keras.optimizers import SGD
from keras.utils import to_categorical

import speech_recognition as sr
import pyttsx3

# Initialize the recognizer
r = sr.Recognizer()

engine = pyttsx3.init()  # object creation
voices = engine.getProperty("voices")  # getting details of current voice
engine.setProperty("voice", voices[1].id)


# Function to convert text to
# speech
def SpeakText(command):
    # Initialize the engine
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


from gtts import gTTS
from IPython.display import Audio

# speech recognition
while 1:
    a = input("Do you want to ask one more question y/n : ")

    if a in "yY":
        ans = ""
        n = 0
        print("*" * 100)
        print("Listening ... ")
        print("*" * 100)
        while n < 1:
            # Exception handling to handle
            # exceptions at the runtime
            try:
                # use the microphone as source for input.
                with sr.Microphone() as source2:
                    # wait for a second to let the recognizer
                    # adjust the energy threshold based on
                    # the surrounding noise level
                    r.adjust_for_ambient_noise(source2, duration=0.2)

                    # listens for the user's input
                    audio2 = r.listen(source2)
                    print(dir(r.listen))

                    # TO-DO: Change to VOSK API
                    # Using google to recognize audio
                    MyText = r.recognize_google(audio2)

                    question = MyText

            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))

            except sr.UnknownValueError:
                print("unknown error occurred")

            n += 1
        print("Finish")

        # speech recognition over

        # get the ouput and store it in question

        maxLen = 18
        nlu = IntentClassifier(classes, model, tokenizer, label_encoder)
        intent = nlu.get_intent(question)

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

        print(ans)
        SpeakText(ans)
    else:
        break
