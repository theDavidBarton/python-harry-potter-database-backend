from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from re import search
import re

app = Flask(__name__)
CORS(app, origins=['https://the-harry-potter-database-frontend.onrender.com',
     'https://thedavidbarton.github.io'])

# Load JSON data from files
with open('resources/categories.json', encoding='utf8') as categories_file:
    categories = json.load(categories_file)

with open('resources/books.json', encoding='utf8') as books_file:
    books = json.load(books_file)

with open('resources/characters.json', encoding='utf8') as characters_file:
    characters = json.load(characters_file)

with open('resources/spells.json', encoding='utf8') as spells_file:
    spells = json.load(spells_file)

with open('resources/potions.json', encoding='utf8') as potions_file:
    potions = json.load(potions_file)

# Helper function for searching


def search_data(data, query):
    query_regex = '.*' + query + '.*'
    results = [item for item in data if search(
        query_regex, item.get('name', item.get('title')), re.IGNORECASE)]
    return results

# Health check endpoint


@app.route('/health')
def health():
    return jsonify({'status': 'OK'})

# Categories endpoints


@app.route('/api/1/categories', methods=['GET'])
@app.route('/api/1/categories/', methods=['GET'])
def get_categories():
    return jsonify(categories)


@app.route('/api/1/categories/<int:id>', methods=['GET'])
def get_category_by_id(id):
    category = next((cat for cat in categories if cat['id'] == id), None)
    if category:
        return jsonify([category])
    return jsonify({'error': 'no such id!'}), 404

# Books endpoints


@app.route('/api/1/books', methods=['GET'])
def get_books():
    query = request.args.get('search')
    if query:
        results = search_data(books, query)
        return jsonify(results)
    return jsonify(books)


@app.route('/api/1/books/all', methods=['GET'])
def get_all_books():
    return jsonify(books)


@app.route('/api/1/books/<int:id>', methods=['GET'])
def get_book_by_id(id):
    book = next((b for b in books if b['id'] == id), None)
    if book:
        return jsonify([book])
    return jsonify({'error': 'no such id!'}), 404

# Characters endpoints


@app.route('/api/1/characters', methods=['GET'])
def get_characters():
    query = request.args.get('search')
    if query:
        results = search_data(characters, query)
        results = sorted(results, key=lambda x: len(
            x['books_featured_in']), reverse=True)
        return jsonify(results)
    return jsonify(characters)


@app.route('/api/1/characters/all', methods=['GET'])
def get_all_characters():
    return jsonify(characters)


@app.route('/api/1/characters/<int:id>', methods=['GET'])
def get_character_by_id(id):
    character = next((char for char in characters if char['id'] == id), None)
    if character:
        return jsonify([character])
    return jsonify({'error': 'no such id!'}), 404

# Spells endpoints


@app.route('/api/1/spells', methods=['GET'])
def get_spells():
    query = request.args.get('search')
    if query:
        results = search_data(spells, query)
        return jsonify(results)
    return jsonify(spells)


@app.route('/api/1/spells/all', methods=['GET'])
def get_all_spells():
    return jsonify(spells)


@app.route('/api/1/spells/<int:id>', methods=['GET'])
def get_spell_by_id(id):
    spell = next((s for s in spells if s['id'] == id), None)
    if spell:
        return jsonify([spell])
    return jsonify({'error': 'no such id!'}), 404

# Potions endpoints


@app.route('/api/1/potions', methods=['GET'])
def get_potions():
    query = request.args.get('search')
    if query:
        results = search_data(potions, query)
        return jsonify(results)
    return jsonify(potions)


@app.route('/api/1/potions/all', methods=['GET'])
def get_all_potions():
    return jsonify(potions)


@app.route('/api/1/potions/<int:id>', methods=['GET'])
def get_potion_by_id(id):
    potion = next((p for p in potions if p['id'] == id), None)
    if potion:
        return jsonify([potion])
    return jsonify({'error': 'no such id!'}), 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
