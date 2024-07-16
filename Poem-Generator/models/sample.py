import numpy as np
import sys
import random

def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def generate_text(model, text, chars, char_indices, num_chars, maxlen, temperatures=[0.2, 0.5, 1.0, 1.2], length=400):
    start_index = random.randint(0, len(text) - maxlen - 1)
    generated_text = text[start_index: start_index + maxlen]
    
    for temperature in temperatures:
        print('------ temperature:', temperature)
        sys.stdout.write(generated_text)
        
        for i in range(length):
            sampled = np.zeros((1, maxlen, num_chars), dtype=bool)
            for t, char in enumerate(generated_text):
                sampled[0, t, char_indices[char]] = True
            
            preds = model.predict(sampled, verbose=0)[0]
            next_index = sample(preds, temperature)
            next_char = chars[next_index]
            
            generated_text += next_char
            generated_text = generated_text[1:]
            
            sys.stdout.write(next_char)
            sys.stdout.flush()
        print()

