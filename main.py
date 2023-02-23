# Made by William Rubio on February 2023
import tensorflow as tf
import os

# GPU memory growth limiter
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

