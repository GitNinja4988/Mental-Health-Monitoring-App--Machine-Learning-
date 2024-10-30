import cv2
import random
import time
from deepface import DeepFace

# Mood activity mapping
mood_activity_mapping = {
    "happy": ["Go for a dance class", "Have a picnic with friends", "Visit a zoo or aquarium", "Take a pottery class"],
    "sad": ["Watch a feel-good movie", "Journal about your feelings", "Create a simple meal plan for the week"],
    "angry": ["Practice deep breathing exercises", "Go for a run", "Organize your thoughts by journaling"],
    "neutral": ["Read a book", "Try meditating", "Do a simple breathing exercise"]
}

def suggest_activity_based_on_mood(mood):
    activities = mood_activity_mapping.get(mood, [])
    return random.choice(activities) if activities else "No activity suggestion available."

# Real-time facial expression detection with DeepFace
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No camera detected. Exiting...")
else:
    # Countdown before taking the photo
    countdown_time = 10
    for i in range(countdown_time, 0, -1):
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame.")
            break

        # Display countdown message
        cv2.putText(frame, 'Please make a face of how you are feeling right now!', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(frame, f'Countdown: {i}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

        cv2.imshow('Facial Expression Recognition', frame)
        cv2.waitKey(1)  # Display the frame

        time.sleep(1)  # Pause for 1 second for countdown

    # Close the countdown display
    cap.release()
    cv2.destroyAllWindows()

    # Reopen the camera to capture the user's frame after the countdown
    cap = cv2.VideoCapture(0)
    ret, captured_frame = cap.read()
    if not ret:
        print("Failed to capture frame.")
    else:
        # Analyze the captured frame
        try:
            result = DeepFace.analyze(captured_frame, actions=['emotion'], enforce_detection=False)
            mood = result[0]['dominant_emotion']  # Get the dominant emotion
            activity_suggestion = suggest_activity_based_on_mood(mood)

            # Display mood and activity on the screen
            cv2.putText(captured_frame, f'Mood: {mood}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(captured_frame, f'Suggested Activity: {activity_suggestion}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Show the captured frame with results
            cv2.imshow('Facial Expression Recognition', captured_frame)
            cv2.waitKey(5000)  # Show the result for 5 seconds

            # Print debug information
            print(f'Predicted mood: {mood}')
            print(f'Suggested activity: {activity_suggestion}')

        except Exception as e:
            print(f"Error in DeepFace analysis: {e}")

cap.release()
cv2.destroyAllWindows()
