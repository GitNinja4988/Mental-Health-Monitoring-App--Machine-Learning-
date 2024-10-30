import cv2
import numpy as np
import tensorflow as tf

# Load the trained model
model = tf.keras.models.load_model('facial_expression_model.keras')

# Define your emotion labels (adjust based on your dataset)
emotion_labels = ["Happy", "Sad", "Angry", "Neutral", "Surprise", "Fear", "Disgust"]

# Set parameters
picture_size = 48

# Open the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No camera detected. Exiting...")
else:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame.")
            break

        # Convert the frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized_frame = cv2.resize(gray_frame, (picture_size, picture_size))
        
        # Normalize and reshape for model input
        input_frame = resized_frame / 255.0
        input_frame = np.reshape(input_frame, (1, picture_size, picture_size, 1))

        # Predict the expression
        prediction = model.predict(input_frame)
        emotion = emotion_labels[np.argmax(prediction)]

        # Display results on the frame
        cv2.putText(frame, f'Emotion: {emotion}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        
        # Show the frame
        cv2.imshow('Facial Expression Recognition', frame)

        # Break loop on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
