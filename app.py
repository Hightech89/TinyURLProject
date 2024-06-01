from flask import Flask, request, jsonify, redirect
import sqlite3
import string
import random

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY, long_url TEXT, short_code TEXT)')
    conn.commit()
    conn.close()

# URL Shortener function
def generate_short_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.json.get('longUrl')
    short_code = generate_short_code()
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO urls (long_url, short_code) VALUES (?, ?)', (long_url, short_code))
    conn.commit()
    conn.close()
    short_url = request.host_url + short_code
    return jsonify({'shortUrl': short_url})

@app.route('/<short_code>')
def redirect_to_long_url(short_code):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT long_url FROM urls WHERE short_code = ?', (short_code,))
    result = c.fetchone()
    conn.close()
    if result:
        return redirect(result[0])
    else:
        return 'URL not found', 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)