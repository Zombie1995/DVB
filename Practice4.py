import pyttsx3
import pyaudio
import vosk

# Ответы на команды
commands = {
    "привет": "здарова",
    "как дела": "да потихоньку",
    "пока": "давай"
}

# Инициализируем голос
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Инициализируем модель для распознования голоса
model = vosk.Model("./vosk-model-small-ru-0.4")
recognizer = vosk.KaldiRecognizer(model, 16000)

# Инициализируем поток для записи голоса
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)

# Это надо было, чтобы проверить, что голос записывается
# import wave
# wf = wave.open("output.wav", 'wb')
# wf.setnchannels(1)
# wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
# wf.setframerate(16000)
# data = stream.read(16000 * 2)
# wf.writeframes(data)
# wf.close()

SECONDS_TO_LISTEN = 4

# Функция для распознования голоса
def recognize_speech():
    data = stream.read(16000 * SECONDS_TO_LISTEN)
    
    if len(data) == 0:
        return None
    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()
        return result
    else:
        return None

# Главный цикл
is_running = True
while is_running:
    # Обозначаем начало
    engine.say("Маруся слушает")
    engine.runAndWait()

    # Распознаем команду
    command = recognize_speech()

    # Если распознана
    if command is not None:
        # Переводим в нижний регистр
        command = command.lower()
        # Пробегаемся по всем командам и ищем совпадение
        not_found = True
        for keyword, response in commands.items():
            # Если нашли
            if keyword in command:
                engine.say(response)
                engine.runAndWait()
                not_found = False
                if keyword == "пока":
                    is_running = False
                break
        # Если не нашли
        if not_found:
            engine.say(f"Нет команды {command}")
            engine.runAndWait()
    else:
        engine.say("Не распознано")
        engine.runAndWait()

# Очищение
stream.stop_stream()
stream.close()
p.terminate()