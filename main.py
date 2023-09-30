import json
import speech_rec as sr
import translate as ts

ans = "n"
while 1:
    que = sr.speech_rec()
    que = json.loads(que)
    que = que["text"]
    print(que)
    que = ts.translate_hi_en(que)
    print(que)
    ans = input("Do you want to ask one more question y/n : ")
    if ans in "nN":
        break
