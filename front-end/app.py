from flask import Flask, request, render_template, jsonify, send_file
import phe as paillier
import json
import os

app = Flask(__name__)

FILES_DIR = 'D:\\Mini-Project\\front-end\\files'
if not os.path.exists(FILES_DIR):
    os.makedirs(FILES_DIR)

def generate_keys():
    public_key, private_key = paillier.generate_paillier_keypair()
    keys = {}
    keys['public_key'] = {'n': public_key.n}
    keys['private_key'] = {'p': private_key.p, 'q': private_key.q}
    with open(os.path.join(FILES_DIR, 'keys.json'), 'w') as file:
        json.dump(keys, file, indent=2)

def get_keys():
    with open(os.path.join(FILES_DIR, 'keys.json'), 'r') as file:
        keys = json.load(file)
        public_key = paillier.PaillierPublicKey(n=int(keys['public_key']['n']))
        private_key = paillier.PaillierPrivateKey(public_key, keys['private_key']['p'], keys['private_key']['q'])
        return public_key, private_key

def encrypt_data(public_key, data):
    encrypted_list = [public_key.encrypt(x) for x in data]
    encrypted_data = {}
    encrypted_data['public_key'] = {'n': public_key.n}
    encrypted_data['values'] = [(str(x.ciphertext()), x.exponent) for x in encrypted_list]
    return encrypted_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json['data']
    generate_keys()
    public_key, private_key = get_keys()
    encrypted_data = encrypt_data(public_key, data)

    with open(os.path.join(FILES_DIR, 'data.json'), 'w') as file:
        json.dump(encrypted_data, file, indent=2)

    return jsonify({"message": "Data encrypted successfully. You can now download the files."})

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    if filename not in ['keys.json', 'data.json']:
        return "File not found", 404

    file_path = os.path.join(FILES_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True)
