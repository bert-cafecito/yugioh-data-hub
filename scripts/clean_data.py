import csv
import json
import os
import sqlite3

def yugiohdb_cards():
    # Load JSON data
    with open('data/raw/yugiohdb/cards.json') as f:
        data = json.load(f)

    # Connect to SQLite database
    conn = sqlite3.connect("data/processed/yugiohdb.db")
    c = conn.cursor()

    # Create card_sets table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER
        )
    ''')

    # Create processed data directory
    if not os.path.exists('data/processed/yugiohdb'):
        os.makedirs('data/processed/yugiohdb')

    # Prepare CSV files
    cards_file = open('data/processed/yugiohdb/cards.csv', 'w', newline='')
    card_sets_file = open('data/processed/yugiohdb/card_sets.csv', 'w', newline='')

    cards_writer = csv.writer(cards_file)
    card_set_writer = csv.writer(card_sets_file)

    # Write CSV headers
    cards_writer.writerow(['id', 'card_data'])
    card_set_writer.writerow(['card_id', 'release_date', 'card_number', 'name', 'rarity', 'extracted_date'])

    # Assign unique ID to each card and write data
    card_id = 1
    for card in data:
        extracted_date = card['extracted_date']

        # Delete extracted_date from card
        del card['extracted_date']

        # Write card data by row
        for card_set in card['card_sets']:
            # Write set data by card
            card_set_writer.writerow([
                card_id, 
                card_set['set_release_date'], 
                card_set['set_card_number'],
                card_set['set_name'],
                card_set['set_rarity'],
                extracted_date
            ])

        # Delete card_sets from card
        del card['card_sets']
        
        cards_writer.writerow([card_id, json.dumps(card)])
        card_id += 1
        
    # Close CSV files
    cards_file.close()
    card_sets_file.close()
    
def clean_data():
    yugiohdb_cards()

if __name__ == '__main__':
    clean_data()