import phe as paillier
import json

def generate_keys():

	public_key, private_key = paillier.generate_paillier_keypair()
	keys = {}
	keys['public_key'] = {'n' : public_key.n}
	keys['private_key'] = {'p' : private_key.p, 'q' : private_key.q}
	with open('keys.json', 'w') as file: 
		json.dump(keys, file, indent = 2)

def get_keys():

	with open('keys.json', 'r') as file: 
		keys = json.load(file)
		public_key = paillier.PaillierPublicKey(n = int(keys['public_key']['n']))
		private_key = paillier.PaillierPrivateKey(public_key, keys['private_key']['p'], keys['private_key']['q'])
		return public_key, private_key

def encrypt_data(public_key, data):

	encrypted_list = [public_key.encrypt(x) for x in data]
	encrypted_data = {}
	encrypted_data['public_key'] = {'n': public_key.n}
	encrypted_data['values'] = [(str(x.ciphertext()), x.exponent) for x in encrypted_list]
	return encrypted_data

def get_encrypted_result():
	
    with open('result.json', 'r') as file: 
        data = json.load(file)
        return data

generate_keys()

public_key, private_key = get_keys()

user_data = [40,0,1,140,289,0,0,172,0,0]
res = encrypt_data(public_key, user_data)

with open('data.json', 'w') as file: 
    json.dump(res, file, indent = 2)