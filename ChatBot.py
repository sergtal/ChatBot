import json
import random
import eel
import nltk
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
#загрузка библиотек

config_file = open("my.json", "r", encoding="utf-8_sig")
log_file = open("lu.json", "r", encoding="utf-8_sig")
BOT_CONFIG = json.load(config_file) #загрузка файла для модели
BOT_LOG = json.load(log_file) #загрузка файла для истории сообщений

X = []

for name, data in BOT_CONFIG["intents"].items():
  for example in data["examples"]:
    X.append(example)

vectorizer = CountVectorizer() #подготовка файла для модели
vectorizer.fit(X)

model = joblib.load("./model.joblib") #выгрузка модели

def filter(text): #цензура текста по алфавиту
  alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя -'
  result = [c for c in text if c in alphabet]
  return ''.join(result)

def match(text, example): #цензура текста по нижнему регистру
  text = filter(text.lower())
  example = example.lower()

  distance = nltk.edit_distance(text, example) / len(example)
  return distance < 0.4 #если >40% совпадение в тексте.. можно изменять параметр

def get_intent(text): #нахождение по конкретному интенту 
  for intent in BOT_CONFIG['intents']:
    for example in BOT_CONFIG['intents'][intent]['examples']:
      if match(text, example):
        return intent

def bot(text):  #проверка интента
  intent = get_intent(text) 

  if intent:  #если интент найден
    print("match: "+ intent)
    return random.choice(BOT_CONFIG["intents"][intent]["responses"])

  if not intent:  #если не найден - работа модели
    transformed_text = vectorizer.transform([text])
    intent = model.predict(transformed_text)[0]
    print("model: "+ intent)

  return random.choice(BOT_CONFIG["failure_phrases"]) #если бот не понял

eel.init('web')
@eel.expose  

def recv_data(question):  #функция передачи запрос-ответ от приложения
  if question != "": 
    answer = bot(question) 
    print(f"[Вы]: {question}")
    print(f"[Бот]: {answer}")
    
    a_dict = ([question, answer]) #сохраняет историю в файл "lu"
    BOT_LOG["answer"].append(a_dict)
    with open('lu.json', 'w', encoding="utf-8_sig") as outfile:
      json.dump(BOT_LOG, outfile, ensure_ascii=False, indent=3)
    return answer

eel.start('index.html', size=(700, 700), position=(650,400))  #цикл приложения

   
    