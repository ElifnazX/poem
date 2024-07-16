import numpy as np
import random
import sys
import json
from typing import List, Tuple
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.optimizers import RMSprop
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.utils import to_categorical
from keras.preprocessing.sequence import pad_sequences

def load_poems(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        poems = json.load(file)
    return '\n'.join('\n'.join(poem['icerik']) for poem in poems).lower()

def prepare_data(text: str, maxlen: int, step: int) -> Tuple[List[str], List[str], dict, int]:
    chars = sorted(list(set(text)))
    char_indices = {char: chars.index(char) for char in chars}
    sentences = []
    next_chars = []

    for i in range(0, len(text) - maxlen, step):
        sentences.append(text[i: i + maxlen])
        next_chars.append(text[i + maxlen])

    return sentences, next_chars, char_indices, len(chars)

def data_generator(sentences: List[str], next_chars: List[str], char_indices: dict, 
                   num_chars: int, maxlen: int, batch_size: int) -> Tuple[np.ndarray, np.ndarray]:
    num_samples = len(sentences)
    while True:
        for i in range(0, num_samples, batch_size):
            X = np.zeros((batch_size, maxlen, num_chars), dtype=bool)
            y = np.zeros((batch_size, num_chars), dtype=bool)
            for j, sentence in enumerate(sentences[i:i+batch_size]):
                for t, char in enumerate(sentence):
                    X[j, t, char_indices[char]] = True
                y[j, char_indices[next_chars[i + j]]] = True
            yield X, y

def build_model(maxlen: int, num_chars: int) -> Sequential:
    model = Sequential()
    model.add(LSTM(128, input_shape=(maxlen, num_chars)))
    model.add(Dense(num_chars, activation='softmax'))
    optimizer = RMSprop(learning_rate=0.01)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer)
    return model

def sample(preds: np.ndarray, temperature: float = 1.0) -> int:
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def generate_text(model: Sequential, prompt: str, char_indices: dict, chars: List[str], 
                  maxlen: int, num_chars: int, length: int = 400, temperatures: List[float] = [0.2, 0.5, 1.0, 1.2]) -> None:
    for temperature in temperatures:
        generated_text = prompt.lower()
        print(f'------ temperature: {temperature}')
        sys.stdout.write(generated_text)

        for i in range(length):
            sampled = np.zeros((1, maxlen, num_chars), dtype=bool)
            for t, char in enumerate(generated_text[-maxlen:]):
                if char in char_indices:
                    sampled[0, t, char_indices[char]] = True

            preds = model.predict(sampled, verbose=0)[0]
            next_index = sample(preds, temperature)
            next_char = chars[next_index]

            generated_text += next_char
            sys.stdout.write(next_char)
            sys.stdout.flush()
        print()

if _name_ == "_main_":
    file_path = 'C:/Users/kadir/Downloads/PoemsJson.json'
    
    text = load_poems(file_path)
    
    maxlen = 60
    step = 5

    sentences, next_chars, char_indices, num_chars = prepare_data(text, maxlen, step)
    
    model = build_model(maxlen, num_chars)

    batch_size = 128
    steps_per_epoch = len(sentences) // batch_size

    checkpoint = ModelCheckpoint("best_model.h5", monitor="loss", save_best_only=True)
    early_stopping = EarlyStopping(monitor="loss", patience=10)

    model.fit(data_generator(sentences, next_chars, char_indices, num_chars, maxlen, batch_size),
              steps_per_epoch=steps_per_epoch,
              epochs=60,
              callbacks=[checkpoint, early_stopping])

    prompt = input("Lütfen şiir için bir başlangıç metni girin: ")

    generate_text(model, prompt, char_indices, sorted(char_indices.keys()), maxlen, num_chars)
