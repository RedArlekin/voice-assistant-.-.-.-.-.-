import config
import tts
import stt
import json

import datetime
from fuzzywuzzy import fuzz
from num2words import num2words
import webbrowser
import random

def filter_cmd(voice: str):
    cmd = voice
    print("Функция filter_cmd была вызвана с аргументом:", cmd)

    for x in config.VA_ALIAS:
        if cmd.startswith(x):
            cmd = cmd.replace(x, "").strip()

    for x in config.VA_TBR:
        cmd = cmd.replace(x, "").strip()

    return cmd

def recognize_cmd(cmd: str):
    print("Функция recognize_cmd() была вызвана с аргументом:", cmd)
    rc = {'cmd': '', 'percent': 0}
    for c, v in config.VA_CMD_LIST.items():
        for x in v:
            vrt = fuzz.token_set_ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt
            if vrt == 100:  # Если совпадение точное, сразу вернуть результат
                return rc
    return rc

def execute_cmd(cmd: str):
    if cmd == '':
        tts.va_speak("Я вас не понял. Повторите, пожалуйста.")
    elif cmd == 'help':
        # help
        text = "Я умею: ..."
        text += "произносить время ..."
        text += "рассказывать анекдоты ..."
        text += "и открывать браузер"
        tts.va_speak(text)
        pass
    elif cmd == 'ctime':
        # current time
        now = datetime.datetime.now()
        text = "Сейч+ас " + num2words(now.hour, lang='ru') + " " + num2words(now.minute, lang='ru')
        tts.va_speak(text)

    elif cmd == 'joke':
        jokes = ['Как смеются программисты? ... ехе ехе ехе',
                 'ЭсКьюЭль запрос заходит в бар, подходит к двум столам и спрашивает .. «м+ожно присоединиться?»',
                 'Программист это машина для преобразования кофе в код']

        tts.va_speak(random.choice(jokes))

    elif cmd == 'open_browser':
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open("http://python.org")


def va_respond(result_text: str):
    try:
        result_json = json.loads(result_text)
        recognized_word = result_json.get("text") or result_json.get("partial")
        if recognized_word:
            recognized_word = recognized_word.lower()
            va_alias_lower = [alias.lower() for alias in config.VA_ALIAS]
            if any(recognized_word.startswith(alias) for alias in va_alias_lower):
                key_phrase = next(alias for alias in va_alias_lower if recognized_word.startswith(alias))
                cmd = recognized_word.replace(key_phrase, "").strip()

                for tbr in config.VA_TBR:
                    cmd = cmd.replace(tbr.lower(), "").strip()

                if not cmd:
                    tts.va_speak("Что?")
                elif cmd in [c for cmds in config.VA_CMD_LIST.values() for c in cmds]:
                    cmd_key = next(k for k, v in config.VA_CMD_LIST.items() if cmd in v)
                    filtered_cmd = filter_cmd(cmd_key)
                    execute_cmd(filtered_cmd)
                else:
                    tts.va_speak("Я вас не понял. Повторите, пожалуйста.")
            else:
                print("Речь не начинается с ключевого слова")
        else:
            print("Некорректный формат входных данных")
    except json.JSONDecodeError:
        print("Некорректный формат JSON")

def main():
    print(f"{config.VA_NAME} (v{config.VA_VER}) начал свою работу ...")
    tts.va_speak("Слушаю мой госпадин")
    # Начать прослушивание команд
    result_text = stt.va_listen(va_respond)  # Передаем va_respond в качестве callback
    print("result text1", result_text)

if __name__ == "__main__":
    main()