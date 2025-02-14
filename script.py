import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK with the service account key
cred = credentials.Certificate("project1-se-firebase-adminsdk-fbsvc-662649a1fd.json")  # Replace with the path to your .json file
firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()

# Sample test sentences and labels
test_data = [
    {"sentence": "This is a grammatically correct sentence.", "label": 1},
    {"sentence": "She are going to the store.", "label": 0},
    {"sentence": "He loves programming.", "label": 1},
    {"sentence": "I is going to the park.", "label": 0},
    {"sentence": "The weather is nice today.", "label": 1},
    {"sentence": "I don't know where she gone.", "label": 0}
]

# Upload the test data to Firestore
for index, item in enumerate(test_data):
    # Creating a new document in the "grammar_test_data" collection
    doc_ref = db.collection('grammar_test_data').document(f"sentence_{index+1}")
    doc_ref.set(item)

print("Test sentences uploaded successfully.")
