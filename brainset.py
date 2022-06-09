import json
import random
import nltk
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier


config_file = open("my.json", "r", encoding="utf-8_sig")
BOT_CONFIG = json.load(config_file)

X = []
y = []

for name, data in BOT_CONFIG["intents"].items():
  for example in data["examples"]:
    X.append(example)
    y.append(name)

vectorizer = CountVectorizer()
vectorizer.fit(X)

vecX = vectorizer.transform(X)


model = RandomForestClassifier(n_estimators= 500, min_samples_split=3)
model.fit(vecX, y)
joblib.dump(model, "./model.joblib")
