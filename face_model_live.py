import cv2
import random
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
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame.")
            break

        # Use DeepFace to analyze emotions
        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            mood = result[0]['dominant_emotion']  # Get the dominant emotion
            activity_suggestion = suggest_activity_based_on_mood(mood)

            # Display mood and activity on the screen
            cv2.putText(frame, f'Mood: {mood}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(frame, f'Suggested Activity: {activity_suggestion}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Print debug information
            print(f'Predicted mood: {mood}')

        except Exception as e:
            print(f"Error in DeepFace analysis: {e}")

        cv2.imshow('Facial Expression Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()