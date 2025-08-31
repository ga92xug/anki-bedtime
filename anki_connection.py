import json
import urllib.request
import requests

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def query_anki(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(
        urllib.request.urlopen(
            urllib.request.Request('http://127.0.0.1:8765', requestJson)
        )
    )
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']


def get_due_anki():
    try:
        # Steps 1-2: Get card data from Anki (same as before)
        card_ids = query_anki('findCards', query='deck:"Spanisch 5000" is:due')

        if not card_ids:
            print("No cards due today.")
            return

        notes = query_anki('cardsInfo', cards=card_ids)
        
        # 1. To sort like Anki (oldest due cards first):
        sorted_notes = sorted(notes, key=lambda card: card['due'])
        
        # 2. To sort by difficulty (most forgotten cards first):
        # sorted_notes = sorted(notes, key=lambda card: card['lapses'], reverse=True)
        

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Anki.")
        print("Please ensure Anki is running with the AnkiConnect add-on enabled.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise e
    
    return sorted_notes


def close_anki():
    """Tells Anki to close gracefully via AnkiConnect."""
    try:
        print("Sending command to close Anki...")
        query_anki('guiExitAnki')
    except requests.exceptions.ConnectionError:
        # Anki might have already closed, which is fine.
        print("Anki already closed.")
    except Exception as e:
        print(f"An error occurred while trying to close Anki: {e}")
