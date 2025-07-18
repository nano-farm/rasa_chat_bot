import firebase_admin
from firebase_admin import credentials, db
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.interfaces import Action
import datetime
import os

# Initialize Firebase once
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-adminsdk.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://biopower-a5e93-default-rtdb.firebaseio.com'
    })

class ActionSaveUnhandledMessage(Action):
    def name(self):
        return "action_save_unhandled_message"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict):

        # Get the last user message
        user_message = tracker.latest_message.get("text")
        intent_name = tracker.latest_message.get("intent", {}).get("name")

        # Only save if it's actually unrecognized
        if intent_name == "nlu_fallback" or intent_name == "None":
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            data = {
                "message": user_message,
                "timestamp": timestamp
            }

            # Save to Firebase under /unhandled_messages
            ref = db.reference('unhandled_messages')
            ref.push(data)

            # Send fallback message to UI
            dispatcher.utter_message(text="Sorry, we don't understand it. Please tell us more.")
        return []
