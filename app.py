from flask import Flask, render_template, request, jsonify
print("Flask imported successfully")
import os
import sqlite3

app = Flask(__name__)
print("Flask app created")
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/upload-found', methods=['POST'])
def upload_found():
    if 'photo' not in request.files:
        return jsonify({'error': 'No photo uploaded'}), 400
    
    file = request.files['photo']
    item_name = request.form.get('item_name')
    finder_name = request.form.get('finder_name')
    finder_contact = request.form.get('finder_contact')
    
    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    conn = sqlite3.connect('lost_found.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO found_items (item_name, photo_path, finder_name, finder_contact) VALUES (?, ?, ?, ?)',
                   (item_name, filename, finder_name, finder_contact))
    conn.commit()
    conn.close()
    
    return jsonify({'success': 'Item added!'}), 201

@app.route('/search-item', methods=['POST'])
def search_item():
    if 'photo' not in request.files:
        return jsonify({'error': 'No photo uploaded'}), 400
    
    conn = sqlite3.connect('lost_found.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, item_name, finder_name, finder_contact FROM found_items')
    items = cursor.fetchall()
    conn.close()
    
    results = []
    for item in items:
        results.append({
            'id': item[0],
            'item_name': item[1],
            'finder_name': item[2],
            'finder_contact': item[3]
        })
    
    return jsonify({'results': results}), 200

@app.route('/search')
def search():
    return render_template('search.html')

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)