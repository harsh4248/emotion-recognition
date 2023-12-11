import tensorflow as tf
import cv2
import numpy as np
from keras.models import load_model

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def predict_image(image):
    class_names = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # stacked_gray_img = np.stack((gray_image,)*3, axis=-1)
    # print('here')
    # cv2.imshow('frame',stacked_gray_img)
    # cv2.waitKey(1)
    resized_image = cv2.resize(gray_image, (48, 48))
    # resized_image2 = cv2.resize(image,(48, 48))
    resized_image = np.expand_dims(resized_image, axis=0)
    # print(resized_image.shape, resized_image2.shape)
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Rescaling(1./255, input_shape=(48, 48, 3)))

    normalized_image = model.predict(resized_image)

    
    loaded_nn_model = load_model('models/model_trained.h5')

    y_predict=loaded_nn_model.predict(normalized_image)

    print(y_predict)

    res = np.argmax(y_predict[0])
    return class_names[res]


def preprocess_image(frame):

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(frame, 1.3, 5)

    if(type(faces) == type(tuple())):
        return (frame, None)
    else:
        print("fffffffffff here ffffffffffffff",faces)
    # Draw a bounding box around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        face_roi = frame[y:y+h, x:x+w]

        emotion = predict_image(face_roi)
        

        text = f"{emotion} emotion"
        cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)

    
    
    return (frame,emotion)