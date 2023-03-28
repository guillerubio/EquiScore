# Made by Guillermo (William) Rubio on February 2023
from tkinter import filedialog

import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from keras.models import load_model
import os


class ModelPlayground:

    def __init__(self):
        pass

    def prediction(self, model_to_use, img_path):
        model = load_model(os.path.join("models", model_to_use))
        img = cv2.imread(img_path)
        resize = tf.image.resize(img, (256, 256))
        ans = model.predict(np.expand_dims(resize / 255, 0))
        return ans[0]

    def simple_prediction(self, model_to_use, img_path):
        possibility_array = self.prediction(model_to_use, img_path)
        max_p = 0
        i = 1
        h_score = 1
        for x in possibility_array:
            if x > max_p:
                max_p = x
                h_score = i
            i = i + 1

        return h_score


# mp = ModelPlayground()
# possibilityArray = mp.prediction("/Users/guille/Documents/GitHub/EquiScore/models/es_dlm_01.h5",
#                               "/Users/guille/Documents/GitHub/EquiScore/test.jpg")
# print("possibilityArray = " + str(possibilityArray))
# max_p = 0
# i = 0
# h_score = 1
# for x in possibilityArray:
#     if x > max_p:
#         max_p = x
#         h_score = i
#     i += 1
#
# #if (h_score != 10):
#     #print("Henneke Score = " + str(h_score))
# #else:
#     #print("Horse Image Not Valid")
#
# print(mp.simple_prediction("/Users/guille/Documents/GitHub/EquiScore/models/es_dlm_01.h5",
#                               "/Users/guille/Documents/GitHub/EquiScore/test.jpg"))
# print(" ---------------         -------")
#
# print(str(mp.simple_prediction("/Users/guille/Documents/GitHub/EquiScore/models/es_dlm_01.h5",
#                               "/Users/guille/Desktop/Henneke/Imagenes/images (65).jpg")))
# print(mp.prediction("/Users/guille/Documents/GitHub/EquiScore/models/es_dlm_01.h5",
#                               "/Users/guille/Desktop/Henneke/Imagenes/images (65).jpg"))
#
# dir = filedialog.askopenfilename(
#                       initialdir=".",
#                       title="Select Image File",
#                       filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")))
# print("ahoraaaaa")
# print(mp.simple_prediction("/Users/guille/Documents/GitHub/EquiScore/models/es_dlm_01.h5",
#                               dir))