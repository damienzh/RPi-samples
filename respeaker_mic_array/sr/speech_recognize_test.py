import speech_recognition as sr
import os

MICROPHONE_INDEX = 0
MICROPHONE_NAME = 'ReSpeaker'

for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
    if MICROPHONE_NAME in name:
        MICROPHONE_INDEX = index

print('using microphone {0} with device index {1}'.format(MICROPHONE_NAME, MICROPHONE_INDEX))

r = sr.Recognizer()
m = sr.Microphone(device_index=MICROPHONE_INDEX)

with m as source:
    r.adjust_for_ambient_noise(source, duration=3)
    r.energy_threshold = 450
    print(r.energy_threshold)
    raw_input("press a then say something: ")
    print("recording")
    audio = r.listen(source, phrase_time_limit=5, timeout=3)

# cn_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'zh-cn')
# param_dir = os.path.join(cn_path, 'zh_cn.cd_cont_5000')
# dic_file = os.path.join(cn_path, 'zh_cn.dic')
# model_file = os.path.join(cn_path, 'zh_cn.lm.bin')

# custom_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'custom_cmd')
# custom_dic = os.path.join(custom_path, '7224.dic')
# custom_lm = os.path.join(custom_path, '7224.lm')

# language_cn = (param_dir, model_file, dic_file)
# custom_cmd = (param_dir, custom_lm, custom_dic)
try:
    # print("Sphinx thinks you said " + r.recognize_sphinx(audio, language=custom_cmd))
    print("Sphinx thinks you said " + r.recognize_sphinx(audio, language='en-US'))
except sr.UnknownValueError:
    print("Sphinx could not understand audio")
except sr.RequestError as e:
    print("Sphinx error; {0}".format(e))
