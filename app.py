from flask import Flask, request, render_template
import joblib
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate('sentimentclassifier-203bd-firebase-adminsdk-fbsvc-3eeeb36ac9.json')  # Path to your Firebase service account key
firebase_admin.initialize_app(cred)
db = firestore.client()

# Load model and vectorizer from GitHub
MODEL_URL = "https://github.com/Michelle1606/LAB_ISA/blob/main/sentiment_analysis_model.pkl"
VECTORIZER_URL = "https://github.com/Michelle1606/LAB_ISA/blob/main/vectorizer.pkl"

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # HTML form for user input

@app.route('/classify', methods=['POST'])
def classify():
    if request.method == 'POST':
        sentence = request.form['sentence']  # Get the input sentence from the form
        
        # Fetch the actual sentiment from Firebase
        docs = db.collection('test_data').where('review', '==', sentence).stream()
        actual_sentiment = None
        for doc in docs:
            actual_sentiment = doc.to_dict().get('sentiment')
        
        if actual_sentiment is None:
            return render_template('result.html', sentence=sentence, result="Not Found in Firebase", actual="N/A", match="N/A")
        
        # Predict the sentiment using the model
        transformed_sentence = vectorizer.transform([sentence])
        prediction = model.predict(transformed_sentence)
        predicted_sentiment = 'positive' if prediction[0] == 1 else 'negative'
        
        # Compare predicted and actual sentiment
        match = "Correct" if predicted_sentiment == actual_sentiment else "Incorrect"
        
        return render_template(
            'result.html',
            sentence=sentence,
            result=predicted_sentiment,
            actual=actual_sentiment,
            match=match
        )

if __name__ == '__main__':
    app.run(debug=True)