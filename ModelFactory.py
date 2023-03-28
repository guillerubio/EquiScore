# Made by Guillermo (William) Rubio on February 2023
import tensorflow as tf
import os
import imghdr
import cv2
import numpy

from matplotlib import pyplot as plt

class ModelFactory:
    def __init__(self):
        pass
    def createModel (self, data_dir, output_dir):
        # GPU memory growth limiter
        gpus = tf.config.experimental.list_physical_devices('GPU')
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)

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
        data = tf.keras.utils.image_dataset_from_directory(data_dir)
        data_iterator = data.as_numpy_iterator()
        batch = data_iterator.next()

        # Images represented as arrays
        print(batch[1])

        fig, ax = plt.subplots(ncols=4, figsize=(20, 20))
        for idx, img in enumerate(batch[0][:4]):
            ax[idx].imshow(img.astype(int))
            ax[idx].title.set_text(batch[1][idx])

        # plt.show()

        """ NOTE: batch[0] contains the numerical values of our images, every batch will consist of 32 images
         of 256x256 pixels and 3 dimensions, coresponding to the RGB"""

        # DATA PREPROCESSING

        data = data.map(lambda x, y: (x / 255, y))  # Transformation in map, x will now be in the 0-1 range
        scaled_iterator = data.as_numpy_iterator()
        scaled_batch = scaled_iterator.next()
        print("Number of batches = " + str(len(data)))
        # Data Split

        train_size = int(len(data) * 0.7)
        val_size = int(len(data) * 0.2) + 1
        test_size = int(len(data) * 0.1) + 1

        print("Data range = (" + str(scaled_batch[0].min()) + ", " + str(scaled_batch[0].max())
              + ") -> should be around (0.0, 1.0)")
        print("Train batches = " + str(train_size))
        print("Validation batches = " + str(val_size))
        print("Test batches = " + str(test_size))
        print("Total batches accounted = " + str(test_size + val_size + train_size) + " should be <= 8")

        train = data.take(train_size)
        val = data.skip(train_size).take(val_size)
        test = data.skip(train_size + val_size).take(test_size)

        # DEEP LEARNING MODEL
        from keras.models import Sequential  # Sequential model building API -> in to out
        from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten  # Layers for our model

        # Model declaration and initialization
        model = Sequential()

        # Adding layers to our model

        # 1st Layer: Convolutional and MaxPooling layer (input)
        model.add(Conv2D(16, (3, 3), 1, activation='relu', input_shape=(256, 256, 3)))
        model.add(MaxPooling2D())  # Data condensation

        # 2nd Layer: Convolutional and MaxPooling layer
        model.add(Conv2D(32, (3, 3), 1, activation='relu'))
        model.add(MaxPooling2D())  # Data condensation

        # 3rd Layer: Convolutional and MaxPooling layer
        model.add(Conv2D(16, (3, 3), 1, activation='relu'))
        model.add(MaxPooling2D())  # Data condensation

        # 4th Layer: Condensation Layer
        model.add(Flatten())

        # 5th and 6th Layer: Fully connected neurons
        model.add(Dense(256, activation='relu'))
        model.add(Dense(10))

        # Model compilation
        model.compile('adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=["accuracy"])
        print()
        print(model.summary())

        # TRAINING
        logdir = 'logs'
        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=logdir)
        hist = model.fit(train, epochs=20, validation_data=val, callbacks=[tensorboard_callback])

        # TRAINING PERFORMANCE: No problems at a first glance
        fig = plt.figure()  # Loss
        plt.plot(hist.history['loss'], color='teal', label='loss')
        plt.plot(hist.history['val_loss'], color='orange', label='val_loss')
        fig.suptitle('Loss', fontsize=20)
        plt.legend(loc="upper left")
        plt.show()

        fig = plt.figure()  # Accuracy
        plt.plot(hist.history['accuracy'], color='teal', label='accuracy')
        plt.plot(hist.history['val_accuracy'], color='orange', label='val_accuracy')
        fig.suptitle('Accuracy', fontsize=20)
        plt.legend(loc="upper left")
        plt.show()

        # PERFORMANCE EVALUATION
        from keras.metrics import Precision, Recall, BinaryAccuracy
        pre = Precision()
        re = Recall()
        acc = BinaryAccuracy()

        """for batch in test.as_numpy_iterator():
            X, y = batch
            yhat = model.predict(X)
            pre.update_state(y, yhat)
            re.update_state(y, yhat)
            acc.update_state(y, yhat)
            print(f"Precision:{pre.result().numpy()}, Recall:{ re.result().numpy()}, Accuracy:{acc.result().numpy}")"""

        # MODEL SAVING
        filename_template = "es_dlm_{:02d}.h5"
        max_number = -1
        for file_name in os.listdir(output_dir):
            if file_name.startswith("es_dlm_") and file_name.endswith(".h5"):
                try:
                    number = int(file_name[7:9])
                    if number > max_number:
                        max_number = number
                except ValueError:
                    pass

        # Construct the next file name in the sequence
        next_number = max_number + 1
        next_file_name = filename_template.format(next_number)

        model.save(os.path.join(output_dir, next_file_name))

# my_model_factory = ModelFactory()
# my_model_factory.createModel("private_data", "models")