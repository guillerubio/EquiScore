# Made by Guillermo (William) Rubio on February 2023
import tensorflow as tf
import os

# GPU memory growth limiter
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

import imghdr
import cv2

data_dir = "data/BCS"
image_exts = ["jpeg", "jpg", "bmp", "png"]

# Database filter
for image_class in os.listdir(data_dir):
    if image_class != ".DS_Store":
        for image in os.listdir(os.path.join(data_dir, image_class)):
            image_path = os.path.join(data_dir, image_class, image)
            try:
                img = cv2.imread(image_path)
                tip = imghdr.what(image_path)
                if tip not in image_exts:
                    print('Image not in ext list {}'.format(image_path))
                    os.remove(image_path)
            except Exception as e:
                print('Issue with image {}'.format(image_path))
                # os.remove(image_path)



