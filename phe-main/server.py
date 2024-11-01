import model
import phe as paillier
import json

def operations_on_encrypted_data(data):
	
	model_coefficients = model.model_output()
	public_key = data['public_key']
	public_key = paillier.PaillierPublicKey(n = int(public_key['n']))
	enc_nums_rec = [paillier.EncryptedNumber(public_key, int(x[0], int(x[1]))) for x in data['values']]
	results = sum([model_coefficients[i] * enc_nums_rec[i] for i in range(len(enc_nums_rec))])
	return results, public_key

def store_encrypted_result(data):
	
	results, public_key = operations_on_encrypted_data(data)
	encrypted_data = {}
	encrypted_data['public_key'] = {'n': public_key.n}
	encrypted_data['values'] = (str(results.ciphertext()), results.exponent)
	return encrypted_data


data = {}

with open('data.json', 'r') as file: 
	data = json.load(file)

result = store_encrypted_result(data)

with open('result.json', 'w') as file: 
	data = json.dump(result, file, indent = 2)
