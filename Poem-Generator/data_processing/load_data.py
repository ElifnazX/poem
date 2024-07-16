#data_processing/load_data.py
import json

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        poems = json.load(file)
    text = '\n'.join('\n'.join(poem['icerik']) for poem in poems).lower()
    return text
