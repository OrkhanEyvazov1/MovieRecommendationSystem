import pickle
import numpy as np

model= pickle.load(open('catboost_model.pkl', 'rb'))

def inference(user_data):
    # Dummy inference functionexit
    return model.predict(user_data)

sample_user_data = [1996, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 197.0, 5.0]

print(inference(sample_user_data))
