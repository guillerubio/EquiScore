# Made by Guillermo (William) Rubio on February 2023
import tensorflow as tf
import os
import imghdr
import cv2
import numpy
from matplotlib import pyplot as plt

# GPU memory growth limiter
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

data_dir = "data"
image_exts = ["jpeg", "jpg", "bmp", "png"]

# Data filter -> No weird images
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

# Data pipeline -> preprocessing and labels from libraries
data = tf.keras.utils.image_dataset_from_directory("data")
data_iterator = data.as_numpy_iterator()
batch = data_iterator.next()

# Images represented as arrays
print(batch[1])

fig, ax = plt.subplots(ncols=4, figsize=(20, 20))
for idx, img in enumerate(batch[0][:4]):
    ax[idx].imshow(img.astype(int))
    ax[idx].title.set_text(batch[1][idx])

#plt.show()

""" NOTE: batch[0] contains the numerical values of our images, every batch will consist of 32 images
 of 256x256 pixels and 3 dimensions, coresponding to the RGB"""

# DATA PREPROCESSING

data = data.map(lambda x,y: (x/255, y)) # Transformation in map, x will now be in the 0-1 range
scaled_iterator = data.as_numpy_iterator()
scaled_batch = scaled_iterator.next()
print(scaled_batch[0].max())
print(len(data))

