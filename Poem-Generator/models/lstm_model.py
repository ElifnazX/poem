from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.optimizers import RMSprop

def build_model(maxlen, num_chars, learning_rate=0.01):
    model = Sequential()
    model.add(LSTM(128, input_shape=(maxlen, num_chars)))
    model.add(Dense(num_chars, activation='softmax'))
    optimizer = RMSprop(learning_rate=learning_rate)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer)
    return model
