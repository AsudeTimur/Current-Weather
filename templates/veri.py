from flask import Flask, jsonify
import json

app = Flask(__name__)

# JSON dosyasını oku ve veriyi yükle
def load_data():
    with open('/Users/asude/Desktop/weather/Current-Weather/templates/data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

@app.route('/get_data', methods=['GET'])
def get_data():
    data = load_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
