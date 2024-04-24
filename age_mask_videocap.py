import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing import image

# Load age estimation model
age_model = load_model('/Users/ulyochoa/Documents/AgeModel/model5Categorical.keras')

# Load mask detection model
mask_model = load_model('/Users/ulyochoa/Documents/AgeModel/model5Binary.keras')

def detect_age(image):
    # Preprocess image
    img = cv2.resize(image, (200, 200))
    img = img.reshape(1, 200, 200, 3).astype('float32')
    img /= 255

    # Predict age
    age_prediction = age_model.predict(img)
    age = int(age_prediction[0])

    return age

def detect_mask(image):
    # Preprocess image
    img = cv2.resize(image, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    # Predict mask
    mask_prediction = mask_model.predict(img)
    mask = "Mask" if mask_prediction[0][0] > 0.5 else "No Mask"

    return mask

def main():
    # Open webcam
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detect face
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            # Draw rectangle around face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Crop face
            face = frame[y:y+h, x:x+w]

            # Detect age
            age = detect_age(face)

            # Detect mask
            mask = detect_mask(face)

            # Display age and mask status
            cv2.putText(frame, f"Age: {age}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Mask: {mask}", (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Display frame
        cv2.imshow('Face Mask Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release video capture
    cap.release()
    cv2.destroyAllWindows()