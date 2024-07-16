from data_processing import load_data, preprocess_data, data_augmentation
from models import build_model, train_model, generate_text, optimize_hyperparameters
from utils import get_user_input
import numpy as np
import os

def main():
    file_path = get_user_input("C:/Users/kadir/Downloads/PoemsJson.json")
    text = load_data(file_path)
    sentences, next_chars, chars, char_indices, num_chars = preprocess_data(text)
    
    # Veri augmentasyonu
    sentences, next_chars = data_augmentation(sentences, next_chars)
    
    # Veri oluşturma
    X = np.zeros((len(sentences), 60, num_chars), dtype=bool)
    y = np.zeros((len(sentences), num_chars), dtype=bool)
    for i, sentence in enumerate(sentences):
        for t, char in enumerate(sentence):
            X[i, t, char_indices[char]] = True
        y[i, char_indices[next_chars[i]]] = True

    # Hiperparametre optimizasyonu
    best_model, best_params = optimize_hyperparameters(X, y)
    print(f"En iyi hiperparametreler: {best_params}")
    
    # Modeli eğit
    train_model(best_model, sentences, next_chars, char_indices, num_chars, maxlen=60)
    
    # Modeli kaydet
    save_path = "path_to_save_model/my_model.h5"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    best_model.save(save_path)
    print(f"Model kaydedildi: {save_path}")
    
    # Metin üret
    generate_text(best_model, text, chars, char_indices, num_chars, maxlen=60)

if __name__ == '__main__':
    main()
