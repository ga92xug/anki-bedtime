import requests
import json
import urllib.error
from python_ntfy import NtfyClient
import os
import subprocess
import time       
from anki_connection import get_due_anki, close_anki

# --- Configuration ---
NTFY_TOPIC = os.getenv("NTFY_TOPIC_ANKI", "your-topic-here")
ANKI_FLATPAK_ID = "net.ankiweb.Anki"


def extract_words_from_notes(notes, limit=50):
    "This is specific to my Anki note structure."
    
    
    processed_notes = {
    }
    for note in notes:
        cardId = note["cardId"]
        fields = note["fields"]
        german = fields["Deutsch"]["value"].replace("<br>", " ")
        spanish = fields["Spanisch"]["value"].replace("<br>", " ")
        if german in ["bitte Seite 3 aufrufen", "Tutorialkarte - bitte Seite 3 aufrufen"]:
            continue

        if len(processed_notes) >= limit:
            break

        processed_notes[cardId] = {
            "german": german,
            "spanish": spanish
        }
        
    return processed_notes


def main(
        send_to_phone=True,
):
    opened_anki = False
    try:
        notes = get_due_anki()
    except urllib.error.URLError:
        subprocess.Popen(['flatpak', 'run', ANKI_FLATPAK_ID])
        time.sleep(10)  # Wait for Anki to start
        opened_anki = True
        notes = get_due_anki()
        

    # limit to 50 notes
    processed_notes = extract_words_from_notes(notes, limit=50)

    # Step 4: Build the prompt (same as before)
    word_list_str = ""
    for cardID, card in processed_notes.items():
        word_list_str += f"{card['spanish']}" + "\n"
    word_list_str = word_list_str
    prompt = (
        "You are an expert Spanish teacher and story teller."
        "Write a story in Spanish with the following words. Repeat the words multiple times for better memorization."
        "The story should be suitable for someone learning Spanish with an B1 level."
        "Please focus on including all of the following words in the story:\n\n"
        f"{word_list_str}"
        "Start the story without any introduction or explanation."
    )
    

    if send_to_phone:
        if NTFY_TOPIC == "your-topic-here":
            raise ValueError("Please set your NTFY_TOPIC environment variable.")
        client = NtfyClient(
            server="https://ntfy.sh",
            topic=NTFY_TOPIC,
            # password=ENCRYPTION_KEY # Use the password for encryption
        )
        client.send(prompt)
        print(f"Successfully sent prompt to ntfy topic: {NTFY_TOPIC}")
    else:
        print(f"Not sending to phone, send_to_phone is False. Topic {NTFY_TOPIC}")
        print(prompt)

    if opened_anki:
        close_anki()
        time.sleep(10)  # Wait for Anki to close


if __name__ == "__main__":
    main()