from flask import Flask, render_template, request, jsonify
from model import predict_sentiment, suggest_activity

# Do not import face model functions here to prevent them from running on server startup
# from face_model_live import process_facial_data_live  
# from face_model_Captured import process_facial_data_captured  

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/mental_health', methods=['GET', 'POST'])
def mental_health():
    if request.method == 'POST':
        user_input = request.json.get('input_field')  # Get user input
        if user_input:
            try:
                sentiment = predict_sentiment(user_input)  # Get sentiment
                activity_suggestion = suggest_activity(sentiment)  # Get activity suggestion
                return jsonify(sentiment=sentiment, activity=activity_suggestion)  # Return JSON response
            except Exception as e:
                return jsonify({'error': str(e)}), 500  # Handle errors gracefully
        return jsonify({'error': 'No input provided'}), 400  # Handle missing input
    return render_template('mental_health.html')

@app.route('/face_recognition', methods=['GET', 'POST'])
def face_recognition():
    if request.method == 'POST':
        # Import face model functions here to ensure they only load when this route is accessed
        from face_model_live import process_facial_data_live  
        from face_model_Captured import process_facial_data_captured  

        action = request.json.get('action')  # Get action from request
        try:
            if action == 'live':
                recognition_result = process_facial_data_live()  # Process live data
                return jsonify(recognition_result)  # Return the result as JSON
            elif action == 'captured':
                # Ensure the function for captured expressions is called here
                recognition_result = process_facial_data_captured()  # No file needed for captured data processing
                return jsonify(recognition_result)  # Return the result as JSON
        except Exception as e:
            return jsonify({'error': str(e)}), 500  # Handle errors gracefully
        
        return jsonify({'error': 'Invalid action provided'}), 400  # Handle invalid action

    return render_template('face_recognition.html')  # Render the template for GET requests


if __name__ == '__main__':
    app.run(debug=True)
