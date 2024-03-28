import os
import imp
import sys
import glob

###### Temp add to get the following library
sys.path.append('C:\\Users\\sebas\\AppData\\Roaming\\Python\\Python310\\site-packages')

import matplotlib.pyplot as plt
import numpy as np
import PIL
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
import pathlib


def createDataset():
	#dataset_url = "https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz"
	datasetDisc = "C:/Users/sebas/Documents/flower_photos.tgz"
	data_dir = tf.keras.utils.get_file('flower_photos.tar', origin=datasetDisc, extract=True)
	data_dir = pathlib.Path(data_dir).with_suffix('')

	image_count = len(list(data_dir.glob('*/*.jpg')))
	print("Amount of images in data set: " + str(image_count))

	###### Create Dataset

	# Init Variable  Lower batch size =  higher accuracy, low resolution help to remove 'noise'
	batch_size = 16
	img_height = 300
	img_width = 300

	# It's good practice to use a validation split when developing your model. Use 80% of the images for training and 20% for validation
	train_ds = tf.keras.utils.image_dataset_from_directory(
		data_dir,
		validation_split=0.2,
		subset="training",
		seed=532,
		image_size=(img_height, img_width),
		batch_size= batch_size
		)
	    
	val_ds = tf.keras.utils.image_dataset_from_directory(
		data_dir,
		validation_split=0.2,
		subset="validation",
		seed=532,
		image_size=(img_height, img_width),
		batch_size= batch_size
		)

	class_names = train_ds.class_names
	print("Classes: " , class_names)

	## Here are the first nine images from the training dataset:
	##plt.figure(figsize=(10, 10))
	##for images, labels in train_ds.take(1):
	##	for i in range(9):
	##		ax = plt.subplot(3, 3, i + 1)
	##		plt.imshow(images[i].numpy().astype("uint8"))
	##		plt.title(class_names[labels[i]])
	##		plt.axis("off")


	## The image_batch is a tensor of the shape (32, 180, 180, 3). 
	## This is a batch of 32 images of shape 180x180x3 (the last dimension refers to color channels RGB). 
	## The label_batch is a tensor of the shape (32,), these are corresponding labels to the 32 images.
	##You can call .numpy() on the image_batch and labels_batch tensors to convert them to a numpy.ndarray.

	for image_batch, labels_batch in train_ds:
		print(image_batch.shape)
		print(labels_batch.shape)
		break

	## Configure the dataset for performance
	AUTOTUNE = tf.data.AUTOTUNE

	train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
	val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

	####################################################### Standardize the data ###################################################
	## The RGB channel values are in the [0, 255] range. This is not ideal for a neural network; in general you should seek to make your input values small.
	## Here, you will standardize values to be in the [0, 1] range by using tf.keras.layers.Rescaling:
	## Normalization of intensity
	normalization_layer = layers.Rescaling(1./255)

	normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
	image_batch, labels_batch = next(iter(normalized_ds))
	first_image = image_batch[0]
	##### Notice the pixel values are now in `[0,1]`.
	print(np.min(first_image), np.max(first_image))

	## init classes of dataset
	num_classes = len(class_names)

	## A basic Keras model
	##Create the model
	##The Keras Sequential model consists of three convolution blocks (tf.keras.layers.Conv2D) with a max pooling layer (tf.keras.layers.MaxPooling2D) in each of them. 
	## There's a fully-connected layer (tf.keras.layers.Dense) with 128 units on top of it that is activated by a ReLU activation function ("relu"). 
	## This model has not been tuned for high accuracy; the goal is to show a standard approach.

	model = Sequential([
		layers.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
		layers.Conv2D(16, 3, padding='same', activation='relu'),
		layers.MaxPooling2D(),
		layers.Conv2D(32, 3, padding='same', activation='relu'),
		layers.MaxPooling2D(),
		layers.Conv2D(64, 3, padding='same', activation='relu'),
		layers.MaxPooling2D(),
		layers.Flatten(),
		layers.Dense(128, activation='relu'),
		layers.Dense(num_classes)
	])


	############################## Data Augmentation to increase accuracy cause of small dataset #############################

	## Consist in transforming pictures to artificially increase dataset

	data_augmentation = keras.Sequential(
	[
		layers.RandomFlip("horizontal",input_shape=(img_height,img_width, 3)),
		layers.RandomRotation(0.15),
		layers.RandomZoom(0.15),
	]
	)

	## Visualize Data example
	#plt.figure(figsize=(10, 10))
	#for images, _ in train_ds.take(1):
		#for i in range(9):
			#augmented_images = data_augmentation(images)
			#ax = plt.subplot(3, 3, i + 1)
			#plt.imshow(augmented_images[0].numpy().astype("uint8"))
			#plt.axis("off")

	# Dropout also
	model = Sequential([
		data_augmentation,
		layers.Rescaling(1./255),
		layers.Conv2D(16, 3, padding='same', activation='relu'),
		layers.MaxPooling2D(),
		layers.Conv2D(32, 3, padding='same', activation='relu'),
		layers.MaxPooling2D(),
		layers.Conv2D(64, 3, padding='same', activation='relu'),
		layers.MaxPooling2D(),
		layers.Dropout(0.2),
		layers.Flatten(),
		layers.Dense(128, activation='relu'),
		layers.Dense(num_classes, name="outputs")
	])

	############################################ Compile Model #############################################
	model.compile(optimizer='adam',loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),metrics=['accuracy'])
	
	########################################### Model Summary ##############################################
	model.summary()

	############################################ Train the model ###########################################
	epochs = 15
	history = model.fit(train_ds, validation_data=val_ds, epochs=epochs)

	######## Convert the model #########
	converter = tf.lite.TFLiteConverter.from_keras_model(model)
	tflite_model = converter.convert()

	########## Save the model ###########
	path = "C:/Users/sebas/Documents/"
	with open(path + 'model.tflite', 'wb') as f:
		f.write( tflite_model)

	################################ Check model############################

	flowerDisc = "C:/Users/sebas/Documents/flowerTestModel.jpg"

	img = tf.keras.utils.load_img(flowerDisc, target_size=(img_height, img_width))
	img_array = tf.keras.utils.img_to_array(img)
	img_array = tf.expand_dims(img_array, 0) # Create a batch

	predictions = model.predict(img_array)
	score = tf.nn.softmax(predictions[0])

	print("This image most likely belongs to {} with a {:.2f} percent confidence.".format(class_names[np.argmax(score)], 100 * np.max(score)))

def visualizeModel(history,epochs,train_ds, img_height,img_width):
	## Visualise Training Accuracy
	acc = history.history['accuracy']
	val_acc = history.history['val_accuracy']

	loss = history.history['loss']
	val_loss = history.history['val_loss']

	epochs_range = range(epochs)

	plt.figure(figsize=(8, 8))
	plt.subplot(1, 2, 1)
	plt.plot(epochs_range, acc, label='Training Accuracy')
	plt.plot(epochs_range, val_acc, label='Validation Accuracy')
	plt.legend(loc='lower right')
	plt.title('Training and Validation Accuracy')

	plt.subplot(1, 2, 2)
	plt.plot(epochs_range, loss, label='Training Loss')
	plt.plot(epochs_range, val_loss, label='Validation Loss')
	plt.legend(loc='upper right')
	plt.title('Training and Validation Loss')
	plt.show()

def loadLiteModel(class_names,TF_MODEL_FILE_PATH):

	class_names = train_ds.class_names

	TF_MODEL_FILE_PATH = 'C:/Users/sebas/Documents/model.tflite' # The default path to the saved TensorFlow Lite model

	interpreter = tf.lite.Interpreter(model_path=TF_MODEL_FILE_PATH)
	#print(interpreter.get_signature_list())

	dicInterpreter = interpreter.get_signature_list()
	sequential = dicInterpreter['serving_default']['inputs'][0]
	print("Sequential to update in the classify_lite: " + sequential)

	interpreter.get_signature_list()
	classify_lite = interpreter.get_signature_runner('serving_default')
	#print(classify_lite)

	return classify_lite

def findTagsPhoto(listPictures,classify_lite):
	##############################
	dataDirToTest = "C:/Users/sebas/Documents/testFlowerModel/"
	listPictures = list(glob.glob(dataDirToTest + '*'))

	for picture in listPictures:
		img = tf.keras.utils.load_img(picture, target_size=(img_height, img_width))
		img_array = tf.keras.utils.img_to_array(img)
		img_array = tf.expand_dims(img_array, 0) # Create a batch

		predictions_lite = classify_lite(sequential_31_input= img_array)['outputs']
		score_lite = tf.nn.softmax(predictions_lite)

		filename = os.path.basename(picture)
		tagMain = class_names[np.argmax(score_lite)
		print("This image " + filename +  " most likely belongs to {} with a {:.2f} percent confidence.".format(class_names[np.argmax(score_lite)], 100 * np.max(score_lite)))


