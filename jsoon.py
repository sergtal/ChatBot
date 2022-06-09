import json


config_file = open("big_bot_config.json", "r", encoding="utf-8_sig")
BOT_CONFIG = json.load(config_file)

with open('lu.json', 'w', encoding="utf-8_sig") as outfile:
    json.dump(BOT_CONFIG, outfile, ensure_ascii=False, indent=3)

