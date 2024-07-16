import numpy as np

def data_generator(sentences, next_chars, char_indices, num_chars, maxlen, batch_size=128):
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

def train_model(model, sentences, next_chars, char_indices, num_chars, maxlen, batch_size=128, epochs=60):
    model.fit(data_generator(sentences, next_chars, char_indices, num_chars, maxlen, batch_size=batch_size),
              steps_per_epoch=len(sentences) // batch_size,
              epochs=epochs)
