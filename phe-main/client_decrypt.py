import json
import phe as paillier

def get_encrypted_result():
    with open('result.json', 'r') as file: 
        data = json.load(file)
        return data
    
def get_keys():
      
	with open('keys.json', 'r') as file: 
		keys = json.load(file)
		public_key = paillier.PaillierPublicKey(n = int(keys['public_key']['n']))
		private_key = paillier.PaillierPrivateKey(public_key, keys['private_key']['p'], keys['private_key']['q'])
		return public_key, private_key


res = get_encrypted_result()

encrypted_result_public_key = paillier.PaillierPublicKey(n = int(res['public_key']['n']))
answer = paillier.EncryptedNumber(encrypted_result_public_key, int(res['values'][0]), int(res['values'][1]))

public_key, private_key = get_keys()

if (encrypted_result_public_key == public_key):
    print("Decrypted Result:", private_key.decrypt(answer))