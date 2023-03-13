# Made by Guillermo (William) Rubio on February 2023
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from keras.models import load_model
import os
import cv2


def prediction(model_to_use, img_path):
    model = load_model(os.path.join("models", img_path))
    img = cv2.imread(model_to_use)
    resize = tf.image.resize(img, (256, 256))
    ans = model.predict(np.expand_dims(resize / 255, 0))
    return str(ans)



class ModelPlayground:

    model = load_model(os.path.join("models", "es_dlm_01.h5"))
    img = cv2.imread("test.jpg")
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()
    resize = tf.image.resize(img, (256, 256))
    ans = model.predict(np.expand_dims(resize / 255, 0))
    possibilityArray = ans[0]
    print("done")
    print("ans = " + str(ans))
    print(ans[0][0])
    bigX = 0
    pos = 1
    posAns = -1
    for x in possibilityArray:
        if (x > bigX):
            bigX = x
            posAns = pos
        pos = pos + 1
    print("Henneke score = " + str(posAns))
