import sqlite3
import random
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report

def setup_database():
    conn = sqlite3.connect('wellness_wave_ml.db')
    cursor = conn.cursor()

    # Create table for words and their sentiment
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS word_sentiment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL,
            sentiment TEXT NOT NULL
        );
    ''')

    # Create table for activities
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity_name TEXT NOT NULL,
            activity_type TEXT NOT NULL,
            activity_description TEXT
        );
    ''')


# Define your sentiments here
    positive_sentiments = [
        ("joyful", "positive"), ("happy", "positive"), ("excited", "positive"), ("delighted", "positive"),
        ("elated", "positive"), ("content", "positive"), ("cheerful", "positive"), ("hopeful", "positive"),
        ("enthusiastic", "positive"), ("grateful", "positive"), ("thrilled", "positive"), ("loved", "positive"),
        ("proud", "positive"), ("relaxed", "positive"), ("satisfied", "positive"), ("inspired", "positive"),
        ("caring", "positive"), ("amused", "positive"), ("playful", "positive"), ("optimistic", "positive"),
        ("passionate", "positive"), ("confident", "positive"), ("kind", "positive"), ("fascinated", "positive"),
        ("motivated", "positive"), ("energetic", "positive"), ("exciting", "positive"), ("hopeful", "positive"),
        ("wonderful", "positive"), ("delighted", "positive"), ("lucky", "positive"), ("free", "positive"),
        ("radiant", "positive"), ("bubbly", "positive"), ("gleeful", "positive"), ("rejuvenated", "positive"),
        ("heartened", "positive"), ("ecstatic", "positive"), ("eager", "positive"), ("resourceful", "positive"),
        ("fulfilled", "positive"), ("refreshed", "positive"), ("optimistic", "positive"), ("alive", "positive"),
        ("wonder", "positive"), ("warm", "positive"), ("peaceful", "positive"), ("calm", "positive"),
        ("jubilant", "positive"), ("cheery", "positive"), ("radiant", "positive"), ("serene", "positive"),
        ("enthusiastic", "positive"), ("carefree", "positive"), ("friendly", "positive"), ("supportive", "positive"),
        ("united", "positive"), ("trusting", "positive"), ("generous", "positive"), ("passionate", "positive"),
        ("blessed", "positive"), ("brilliant", "positive"), ("loving", "positive"), ("thoughtful", "positive"),
        ("zestful", "positive"), ("funny", "positive"), ("delightful", "positive"), ("daring", "positive"),
        ("unique", "positive"), ("spontaneous", "positive"), ("proactive", "positive"), ("dreamy", "positive"),
        ("visionary", "positive"), ("creative", "positive"), ("playful", "positive"), ("zealous", "positive"),
        ("spirit", "positive"), ("charismatic", "positive"), ("passionate", "positive"), ("relatable", "positive"),
        ("uplifted", "positive"), ("spirited", "positive"), ("sincere", "positive"), ("sympathetic", "positive"),
        ("social", "positive"), ("welcoming", "positive"), ("gracious", "positive"), ("sincere", "positive"),
        ("exuberant", "positive"), ("delighted", "positive"), ("heartfelt", "positive"), ("cheery", "positive"),
        ("thoughtful", "positive"), ("kindhearted", "positive"), ("exuberant", "positive"), ("affectionate", "positive"),
        ("sympathetic", "positive"), ("compassionate", "positive"), ("lively", "positive")
    ]

    neutral_sentiments = [
        ("calm", "neutral"), ("content", "neutral"), ("normal", "neutral"), ("indifferent", "neutral"),
        ("average", "neutral"), ("fine", "neutral"), ("okay", "neutral"), ("meh", "neutral"),
        ("neutral", "neutral"), ("unaffected", "neutral"), ("unimpressed", "neutral"), ("passive", "neutral"),
        ("casual", "neutral"), ("unbiased", "neutral"), ("moderate", "neutral"), ("steady", "neutral"),
        ("equable", "neutral"), ("mixed", "neutral"), ("bland", "neutral"), ("mild", "neutral"),
        ("simple", "neutral"), ("ordinary", "neutral"), ("unremarkable", "neutral"), ("mediocre", "neutral"),
        ("unexceptional", "neutral"), ("typical", "neutral"), ("common", "neutral"), ("unfazed", "neutral"),
        ("stagnant", "neutral"), ("calm", "neutral"), ("poised", "neutral"), ("detached", "neutral"),
        ("cool", "neutral"), ("dispassionate", "neutral"), ("tranquil", "neutral"), ("reserved", "neutral"),
        ("sober", "neutral"), ("collected", "neutral"), ("coolheaded", "neutral"), ("levelheaded", "neutral"),
        ("mellow", "neutral"), ("easygoing", "neutral"), ("laid-back", "neutral"), ("untroubled", "neutral"),
        ("unconcerned", "neutral"), ("practical", "neutral"), ("careful", "neutral"), ("controlled", "neutral"),
        ("rational", "neutral"), ("unbiased", "neutral"), ("sensible", "neutral"), ("thoughtful", "neutral"),
        ("stable", "neutral"), ("steady", "neutral"), ("balanced", "neutral"), ("safe", "neutral"),
        ("responsible", "neutral"), ("reasonable", "neutral"), ("methodical", "neutral"), ("neutralized", "neutral"),
        ("adequate", "neutral"), ("mild", "neutral"), ("unemotional", "neutral"), ("dispassionate", "neutral"),
        ("ordinary", "neutral"), ("expected", "neutral"), ("predictable", "neutral"), ("factual", "neutral"),
        ("matter-of-fact", "neutral"), ("reasonable", "neutral"), ("acceptable", "neutral"), ("unremarkable", "neutral"),
        ("unexceptional", "neutral"), ("neutrality", "neutral"), ("standard", "neutral"), ("average", "neutral"),
        ("conventional", "neutral"), ("plain", "neutral"), ("indeterminate", "neutral"), ("mediocre", "neutral"),
        ("nonchalant", "neutral"), ("easy", "neutral"), ("equable", "neutral")
    ]

    negative_sentiments = [
        ("sad", "negative"), ("angry", "negative"), ("anxious", "negative"), ("frustrated", "negative"),
        ("depressed", "negative"), ("disappointed", "negative"), ("stressed", "negative"), ("hurt", "negative"),
        ("overwhelmed", "negative"), ("jealous", "negative"), ("envious", "negative"), ("nervous", "negative"),
        ("fearful", "negative"), ("worried", "negative"), ("irritated", "negative"), ("guilty", "negative"),
        ("ashamed", "negative"), ("unhappy", "negative"), ("lonely", "negative"), ("hopeless", "negative"),
        ("resentful", "negative"), ("disgusted", "negative"), ("defeated", "negative"), ("hurt", "negative"),
        ("embarrassed", "negative"), ("disheartened", "negative"), ("distressed", "negative"), ("sad", "negative"),
        ("unfulfilled", "negative"), ("disconnected", "negative"), ("angry", "negative"), ("critical", "negative"),
        ("miserable", "negative"), ("bitter", "negative"), ("displeased", "negative"), ("despondent", "negative"),
        ("downcast", "negative"), ("irritable", "negative"), ("shocked", "negative"), ("apprehensive", "negative"),
        ("paranoid", "negative"), ("negative", "negative"), ("unmotivated", "negative"), ("disillusioned", "negative"),
        ("scared", "negative"), ("unsettled", "negative"), ("threatened", "negative"), ("resentful", "negative"),
        ("unsafe", "negative"), ("worried", "negative"), ("critical", "negative"), ("defensive", "negative"),
        ("doubtful", "negative"), ("pessimistic", "negative"), ("discouraged", "negative"), ("defeated", "negative"),
        ("vulnerable", "negative"), ("toxic", "negative"), ("sorrowful", "negative"), ("futile", "negative"),
        ("uninspired", "negative"), ("discontented", "negative"), ("unworthy", "negative"), ("neglected", "negative"),
        ("alienated", "negative"), ("insulted", "negative"), ("displeased", "negative"), ("isolated", "negative"),
        ("offended", "negative"), ("unfortunate", "negative"), ("disheartened", "negative"), ("fretful", "negative"),
        ("grieving", "negative"), ("failing", "negative"), ("hopeless", "negative"), ("uncomfortable", "negative"),
        ("shattered", "negative"), ("sadness", "negative"), ("fear", "negative"), ("anger", "negative"),
        ("hatred", "negative"), ("unwelcome", "negative"), ("troubled", "negative"), ("dismayed", "negative"),
        ("exasperated", "negative"), ("wounded", "negative")
    ]

    # Combine all sentiments
    all_sentiments = positive_sentiments + neutral_sentiments + negative_sentiments

    # Example activities dataset
    activities = [
        ("Box Breathing", "Breathing Exercise", "Inhale for 4 seconds, hold for 4, exhale for 4, hold for 4."),
        ("Gratitude Journaling", "Mental Exercise", "Write down three things you’re grateful for."),
        ("Dance to Your Favorite Song", "Physical Activity", "Dance freely to your favorite song to boost energy."),
        ("Progressive Muscle Relaxation", "Mental Exercise", "Tense and relax each muscle group in your body."),
        ("Mindfulness Meditation", "Meditation", "Focus on your breathing and observe your thoughts."),
        ("Nature Walk", "Physical Activity", "Take a walk in nature to reconnect with the environment."),
        ("Listening to Music", "Leisure", "Enjoy your favorite music to lift your spirits."),
        ("Creative Writing", "Mental Exercise", "Write a short story or poem to express your feelings."),
        ("Aromatherapy", "Relaxation", "Use essential oils to enhance relaxation and reduce stress."),
        ("Yoga", "Physical Activity", "Practice yoga to increase flexibility and reduce tension."),
        ("Cooking a New Recipe", "Leisure", "Experiment with cooking a new dish to spark creativity."),
        ("Reading a Book", "Leisure", "Immerse yourself in a book to escape reality."),
        ("Gardening", "Physical Activity", "Connect with nature and grow your plants."),
        ("Visualization", "Mental Exercise", "Visualize your goals and the steps to achieve them."),
        ("Taking a Warm Bath", "Relaxation", "Relax your muscles and calm your mind."),
        ("Creative Arts and Crafts", "Leisure", "Engage in arts and crafts to express your creativity."),
        ("Journaling", "Mental Exercise", "Write about your thoughts and feelings."),
        ("Exercise", "Physical Activity", "Engage in any physical activity you enjoy."),
        ("Guided Meditation", "Meditation", "Follow a guided meditation to relax your mind."),
        ("Breath of Fire", "Breathing Exercise", "A rapid breathing technique to energize the body."),
        ("Digital Detox", "Leisure", "Take a break from screens and digital devices."),
        ("Playing with Pets", "Leisure", "Spend quality time with your pets."),
        ("Decluttering", "Mental Exercise", "Organize your space to create a calming environment."),
        ("Volunteer Work", "Social Activity", "Give back to your community by volunteering."),
        ("Affirmations", "Mental Exercise", "Repeat positive affirmations to boost self-esteem."),
        ("Playing a Musical Instrument", "Leisure", "Play music to express your emotions."),
        ("Singing", "Leisure", "Sing along to your favorite songs to boost your mood."),
        ("Board Games or Puzzles", "Leisure", "Engage in games or puzzles for mental stimulation."),
        ("Photography", "Leisure", "Capture moments and express creativity through photography."),
        ("Walking a Dog", "Physical Activity", "Take your dog for a walk to enjoy fresh air."),
        ("Candle Making", "Creative Activity", "Create your own candles for relaxation."),
        ("Knitting or Crocheting", "Creative Activity", "Engage in a hands-on craft to calm your mind."),
        ("Going for a Bike Ride", "Physical Activity", "Enjoy a bike ride to explore your surroundings."),
        ("Stretching Exercises", "Physical Activity", "Do some gentle stretches to relieve tension."),
        ("Hiking", "Physical Activity", "Explore trails and enjoy the beauty of nature."),
        ("Writing Letters", "Mental Exercise", "Write letters to loved ones or yourself."),
        ("Watching a Favorite Movie", "Leisure", "Enjoy a movie that makes you feel good."),
        ("Building a Model", "Creative Activity", "Construct models as a form of creative expression."),
        ("Making Vision Boards", "Mental Exercise", "Create a visual representation of your goals."),
        ("Learning a New Skill", "Mental Exercise", "Take an online course to learn something new."),
        ("Practicing Mindfulness", "Mental Exercise", "Be present and aware in the moment."),
        ("Scented Candles", "Relaxation", "Light scented candles to create a calming atmosphere."),
        ("Writing Poetry", "Creative Activity", "Express your feelings through poetry."),
        ("Spa Day at Home", "Relaxation", "Create a spa-like atmosphere at home for relaxation."),
        ("Tai Chi", "Physical Activity", "Practice this gentle form of martial arts for relaxation."),
        ("Visiting a Museum", "Leisure", "Explore art and culture in your local museum."),
        ("Fishing", "Leisure", "Relax by the water and enjoy fishing."),
        ("Taking Photos of Nature", "Leisure", "Capture the beauty of nature through photography."),
        ("Hosting a Game Night", "Social Activity", "Invite friends for a fun game night."),
        ("Crafting Scrapbooks", "Creative Activity", "Create a scrapbook to preserve memories."),
        ("Indoor Plant Care", "Leisure", "Take care of your indoor plants to connect with nature."),
        ("Puzzle Solving", "Mental Exercise", "Challenge your mind with puzzles."),
        ("Stargazing", "Leisure", "Spend time outside at night to observe the stars."),
        ("Candlelit Dinner", "Social Activity", "Prepare a nice meal and enjoy it by candlelight."),
        ("Virtual Coffee with Friends", "Social Activity", "Catch up with friends over a video call."),
        ("Baking", "Creative Activity", "Bake something sweet to enjoy or share."),
        ("Making Homemade Gifts", "Creative Activity", "Create personalized gifts for loved ones."),
        ("Going to a Local Event", "Social Activity", "Participate in community events."),
        ("Mindful Eating", "Mental Exercise", "Practice being present during meals."),
        ("Doodling", "Creative Activity", "Draw or doodle for fun."),
        ("Vision Quest", "Spiritual Activity", "Spend time reflecting and seeking personal insights."),
        ("Practicing Gratitude", "Mental Exercise", "Reflect on things you're grateful for."),
        ("Creating a Family Tree", "Mental Exercise", "Explore your ancestry and create a family tree."),
        ("Taking Breaks", "Mental Exercise", "Schedule regular breaks to refresh your mind."),
        ("Intermittent Fasting", "Health Activity", "Try fasting for mental clarity and physical benefits."),
        ("Attend a Workshop", "Mental Exercise", "Learn something new by attending a workshop."),
        ("Create a Blog", "Creative Activity", "Start a blog to share your thoughts and experiences."),
        ("Bike to Work", "Physical Activity", "Bike instead of driving to promote health."),
        ("Practice Self-Compassion", "Mental Exercise", "Be kind to yourself during difficult times."),
        ("Explore New Hobbies", "Creative Activity", "Try out new hobbies that interest you."),
        ("Participate in Community Service", "Social Activity", "Get involved in your local community."),
        ("Cook with Family", "Social Activity", "Prepare a meal together with family or friends."),
        ("Join a Book Club", "Social Activity", "Participate in discussions about books."),
        ("Practice Active Listening", "Social Activity", "Listen attentively in conversations."),
        ("Creating Art", "Creative Activity", "Engage in any form of artistic expression."),
        ("Attend a Yoga Class", "Physical Activity", "Join a yoga class for relaxation and fitness."),
        ("Join a Sports Team", "Physical Activity", "Get active by joining a local sports team."),
        ("Participate in a Charity Run", "Physical Activity", "Run for a cause you care about."),
        ("Engage in Craft Fairs", "Social Activity", "Sell or buy crafts at local fairs."),
        ("Sustainable Living Workshops", "Mental Exercise", "Attend workshops on sustainability practices."),
        ("Hiking Clubs", "Physical Activity", "Join groups to explore hiking trails together."),
        ("Attend Music Festivals", "Leisure", "Enjoy live music and community."),
        ("Watch Documentaries", "Leisure", "Learn about various topics through documentaries."),
        ("Start a Garden", "Creative Activity", "Cultivate a garden for beauty and relaxation."),
        ("Make Seasonal Decorations", "Creative Activity", "Create decorations based on the seasons."),
        ("Potluck Dinner", "Social Activity", "Invite friends to bring a dish and enjoy together."),
        ("Participate in Online Forums", "Social Activity", "Engage in discussions on topics you love."),
        ("Local History Tours", "Leisure", "Explore local history through guided tours."),
        ("Visit National Parks", "Leisure", "Explore the beauty of national parks."),
        ("Mindful Walking", "Mental Exercise", "Practice mindfulness while walking."),
        ("Social Media Break", "Mental Exercise", "Take a break from social media."),
        ("Visit Animal Shelters", "Social Activity", "Spend time with animals in shelters."),
        ("Watch Live Theater", "Leisure", "Experience live performances for entertainment."),
        ("Learn a New Language", "Mental Exercise", "Challenge your mind by learning a new language."),
        ("Participate in a Debate Club", "Social Activity", "Engage in thoughtful discussions."),
        ("Visit Historical Sites", "Leisure", "Explore historical places in your area."),
        ("Start a Podcast", "Creative Activity", "Share your voice and thoughts through podcasts."),
        ("Take Art Classes", "Creative Activity", "Learn new art techniques and styles."),
        ("Join Online Support Groups", "Social Activity", "Engage with others for support."),
        ("Travel to New Places", "Leisure", "Explore new cities or countries."),
        ("Work on a DIY Project", "Creative Activity", "Complete a project at home to improve your space.")
    ]

    # Inserting data into the database
    cursor.executemany('INSERT INTO word_sentiment (word, sentiment) VALUES (?, ?)', all_sentiments)
    cursor.executemany('INSERT INTO activities (activity_name, activity_type, activity_description) VALUES (?, ?, ?)', activities)

    conn.commit()
    conn.close()

def train_model():
    conn = sqlite3.connect('wellness_wave_ml.db')
    cursor = conn.cursor()

    # Fetching data from the database
    cursor.execute('SELECT word, sentiment FROM word_sentiment')
    data = cursor.fetchall()

    # Preparing the dataset for training
    if not data:
        print("No data found for training. Please ensure the database is populated.")
        return

    words, sentiments = zip(*data)
    X_train, X_test, y_train, y_test = train_test_split(words, sentiments, test_size=0.2, random_state=42)

    # Vectorizing the text data
    vectorizer = TfidfVectorizer()
    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)

    # Training the model
    model = RandomForestClassifier()
    model.fit(X_train_vectorized, y_train)

    # Evaluating the model
    y_pred = model.predict(X_test_vectorized)
    print(f'Accuracy: {accuracy_score(y_test, y_pred)}')
    print(f'Classification Report:\n{classification_report(y_test, y_pred)}')

    # Saving the model and vectorizer
    joblib.dump(model, 'sentiment_model.pkl')
    joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')

    conn.close()

def predict_sentiment(user_input):
    # Check if model and vectorizer files exist
    if not os.path.exists('sentiment_model.pkl') or not os.path.exists('tfidf_vectorizer.pkl'):
        print("Model files not found. Please train the model first.")
        return None

    # Load the trained model and vectorizer
    model = joblib.load('sentiment_model.pkl')
    vectorizer = joblib.load('tfidf_vectorizer.pkl')

    # Transform the user input
    input_vectorized = vectorizer.transform([user_input])

    # Predict the sentiment
    prediction = model.predict(input_vectorized)
    return prediction[0]
import random

def suggest_activity(sentiment):
    # Define activities based on sentiment
    activities = {
        "positive": [
            "Engage in physical activities like dance or yoga.",
            "Go for a run or a bike ride in the park.",
            "Participate in a fun workout class, like Zumba or kickboxing.",
            "Take a trip to the beach or a nearby lake for a swim.",
            "Join a sports team or play a game with friends.",
            "Try a new hobby, such as painting, photography, or pottery.",
            "Cook a healthy meal or bake a favorite treat.",
            "Attend a live music concert or community event.",
            "Volunteer for a local charity or community service project.",
            "Spend time with friends and family, enjoying good conversation and laughter."
        ],
        "neutral": [
            "Consider taking a nature walk or journaling.",
            "Read a book that interests you or explore a new genre.",
            "Start a puzzle or play board games with friends or family.",
            "Listen to a podcast or audiobook while relaxing at home.",
            "Watch a movie or binge-watch a new series.",
            "Experiment with cooking a new recipe or trying a new cuisine.",
            "Take a leisurely stroll around your neighborhood or a nearby park.",
            "Spend time organizing or redecorating your living space.",
            "Try a new craft or DIY project.",
            "Engage in gardening or caring for houseplants."
        ],
        "negative": [
            "Try some mindfulness meditation or deep breathing exercises.",
            "Reach out to a trusted friend or family member for support.",
            "Practice self-care routines, like taking a long bath or pampering yourself.",
            "Write down your feelings in a journal to process your emotions.",
            "Engage in gentle exercises like stretching, yoga, or tai chi.",
            "Take a break from social media and spend time offline.",
            "Create a gratitude list, focusing on the positive aspects of your life.",
            "Listen to calming music or nature sounds to help soothe your mind.",
            "Seek professional help or counseling if feelings persist.",
            "Attend a support group or community workshop for mental wellness."
        ]
    }

    # Return a random activity based on the sentiment
    if sentiment in activities:
        return random.choice(activities[sentiment])
    else:
        return "No activity suggestion available."


def main():
    setup_database()  # Setup the database and populate it
    train_model()     # Train the model

    while True:
        user_input = input("Enter a word or phrase to analyze its sentiment (or type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        if not user_input.strip():  # Input validation
            print("Please enter a valid word or phrase.")
            continue
        sentiment = predict_sentiment(user_input)
        if sentiment:
            print(f"The predicted sentiment is: {sentiment}")
            activity_suggestion = suggest_activity(sentiment)
            print(f"Suggested activity: {activity_suggestion}")

if __name__ == "__main__":
    main()
