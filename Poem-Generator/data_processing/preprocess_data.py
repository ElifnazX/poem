import numpy as np
import re

def clean_text(text):    
    text = text.lower()
    text = re.sub(r'\s+', ' ', text) 
    text = re.sub(r'[^\w\s]', '', text) 
    return text

def preprocess_data(text, maxlen=60, step=5):
    text = clean_text(text)
    
    chars = sorted(list(set(text)))
    char_indices = {char: chars.index(char) for char in chars}
    num_chars = len(chars)
    
    sentences = []
    next_chars = []
    
    for i in range(0, len(text) - maxlen, step):
        sentences.append(text[i: i + maxlen])
        next_chars.append(text[i + maxlen])
    
    return sentences, next_chars, chars, char_indices, num_chars

def data_augmentation(sentences, next_chars):
    augmented_sentences = sentences.copy()
    augmented_next_chars = next_chars.copy()
    
    # Basit veri augmentasyonu: cümleleri ters çevirme
    for sentence in sentences:
        augmented_sentences.append(sentence[::-1])
    for next_char in next_chars:
        augmented_next_chars.append(next_char)
    
    return augmented_sentences, augmented_next_chars
