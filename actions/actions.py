import os
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionSaveUserMessage(Action):
    def name(self) -> str:
        return "action_save_user_message"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict):
        """
        Saves the latest user message to Firebase Realtime Database.
        """
        user_message = tracker.latest_message.get('text')
        payload = {
            "sender": tracker.sender_id,
            "message": user_message
        }

        # Use environment variable for the Firebase URL, fallback to default if not set
        firebase_url = os.getenv("FIREBASE_DB_URL", "https://biopower-a5e93-default-rtdb.firebaseio.com/messages.json")

        try:
            response = requests.post(firebase_url, json=payload, timeout=5)
            response.raise_for_status()
            dispatcher.utter_message(text="Your message has been saved!")
        except requests.RequestException as e:
            dispatcher.utter_message(text=f"Failed to save your message: {e}")

        return []
