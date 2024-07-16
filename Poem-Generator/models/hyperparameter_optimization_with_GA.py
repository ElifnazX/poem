from keras.wrappers.scikit_learn import KerasClassifier
from skopt import gp_minimize
from skopt.space import Integer, Real
from skopt.utils import use_named_args
from .model_architecture import build_model
import numpy as np

# Hiperparametre alanlarını tanımlama
space  = [
    Integer(32, 256, name='lstm_units'),
    Real(1e-4, 1e-1, "log-uniform", name='learning_rate'),
    Integer(10, 50, name='epochs'),
    Integer(32, 256, name='batch_size')
]

@use_named_args(space)
def fitness(lstm_units, learning_rate, epochs, batch_size):
    model = KerasClassifier(build_fn=build_model, lstm_units=lstm_units, learning_rate=learning_rate, epochs=epochs, batch_size=batch_size, verbose=0)
    model.fit(X_train, y_train)
    accuracy = model.score(X_valid, y_valid)
    return -accuracy

def optimize_hyperparameters(X, y):
    global X_train, X_valid, y_train, y_valid

    # Veriyi eğitim ve doğrulama setlerine ayır
    from sklearn.model_selection import train_test_split
    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)

    res = gp_minimize(fitness, space, n_calls=30, random_state=42)
    
    best_params = {dim.name: val for dim, val in zip(space, res.x)}
    best_model = build_model(**best_params)
    
    return best_model, best_params

