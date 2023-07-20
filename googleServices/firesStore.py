import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
def fireStoreConnector():

    cred = credentials.Certificate('firedetection.json')

    app = firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db

# doc_ref = db.collection("users").document("alovelace")
# doc_ref.set({"first": "Ada", "last": "Lovelace", "born": 1815})
# doc_ref = db.collection("users").document("aturing")
# doc_ref.set({"first": "Alan", "middle": "Mathison", "last": "Turing", "born": 1912})
#
# users_ref = db.collection("users")
# docs = users_ref.stream()
#
# for doc in docs:
#     print(f"{doc.id} => {doc.to_dict()}")
