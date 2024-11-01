from flask import Flask, render_template, request, jsonify
import model
import phe as paillier
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compute', methods=['POST'])
def compute():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        data = json.load(file)
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON file'}), 400

    try:
        result = store_encrypted_result(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def operations_on_encrypted_data(data):
    model_coefficients = model.model_output()
    public_key_data = data['public_key']
    
    if not public_key_data or 'n' not in public_key_data:
        raise ValueError("Public key is missing or improperly formatted in the input data")

    public_key = paillier.PaillierPublicKey(n=int(public_key_data['n']))
    enc_nums_rec = [paillier.EncryptedNumber(public_key, int(x[0]), int(x[1])) for x in data['values']]
    results = sum([model_coefficients[i] * enc_nums_rec[i] for i in range(len(enc_nums_rec))])
    return results, public_key

def store_encrypted_result(data):
    results, public_key = operations_on_encrypted_data(data)
    encrypted_data = {}
    encrypted_data['public_key'] = {'n': str(public_key.n)}  
    encrypted_data['values'] = (str(results.ciphertext()), results.exponent)
    return encrypted_data

if __name__ == '__main__':
    app.run(debug=True)
