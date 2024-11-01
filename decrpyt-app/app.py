from flask import Flask, request, render_template, jsonify
import json
import phe as paillier

app = Flask(__name__)

def get_keys(keys_data):
    try:
        n = keys_data['public_key'].get('n')
        p = keys_data['private_key'].get('p')
        q = keys_data['private_key'].get('q')

        if n is None or p is None or q is None:
            raise ValueError("Missing key values in keys.json")

        n = int(n)
        public_key = paillier.PaillierPublicKey(n=n)
        private_key = paillier.PaillierPrivateKey(public_key, int(p), int(q))
        return public_key, private_key
    except KeyError as e:
        raise KeyError(f"Missing key: {e}")
    except ValueError as e:
        raise ValueError(f"Invalid key format: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'result_file' not in request.files or 'keys_file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    result_file = request.files['result_file']
    keys_file = request.files['keys_file']
    
    if result_file.filename == '' or keys_file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    try:
        result_data = json.load(result_file)
        keys_data = json.load(keys_file)

        public_key_data = result_data.get('public_key')
        values_data = result_data.get('values')

        if public_key_data is None:
            raise ValueError("Missing 'public_key' in result.json")
        if values_data is None:
            raise ValueError("Missing 'values' in result.json")

        n = public_key_data.get('n')
        if n is None:
            raise ValueError("Missing 'n' in result.json public_key")
        
        if not isinstance(n, int):
            n = int(n)

        if not isinstance(values_data, list) or len(values_data) != 2:
            raise ValueError("Invalid 'values' format in result.json. Expected a list of two integers.")
        
        if not all(isinstance(v, (str, int)) for v in values_data):
            raise ValueError("Invalid 'values' content in result.json. Expected list items to be integers or strings.")

        values_data = [int(v) for v in values_data]

        encrypted_result_public_key = paillier.PaillierPublicKey(n=n)
        answer = paillier.EncryptedNumber(encrypted_result_public_key, values_data[0], values_data[1])

        public_key, private_key = get_keys(keys_data)
        
        if encrypted_result_public_key == public_key:
            decrypted_result = private_key.decrypt(answer)
            return jsonify({"decrypted_result": decrypted_result}), 200
        else:
            return jsonify({"error": "Public key mismatch"}), 400
    except (KeyError, ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
