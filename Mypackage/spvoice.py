# encoding:utf-8
import win32com.client
import json
import os

where_script = os.path.split(os.path.realpath(__file__))[0]

f = open(where_script + '/spvoicesetting.json', 'r')
voicejson = json.load(f)
f.close()

def speak(content):
    spk = win32com.client.Dispatch("SAPI.SpVoice")
    spk.volume = int(voicejson["volume"])  # 音量，范围0~100
    spk.rate = int(voicejson["rate"])     # 语速，范围-10~10
    spk.Speak(content)
    return

