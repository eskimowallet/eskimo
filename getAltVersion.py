import json

b58_digits = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def base58_to_hex(b58str):
  	n = 0
  	for s in b58str:
  		n *= 58
    		digit = b58_digits.index(s)
    		n += digit
  	return hex(n)
  	
def getPrivKey():
	cur = raw_input('Currency? : ')
	privK = raw_input('Private Key : ')
	hexK = base58_to_hex(privK)
	prefix = hexK[0:3]
	i = 3
	while int(prefix, 16) < 128:
		prefix += hexK[i]
		i += 1
	with open('AltCoinVersionPrefixes', 'r') as file:
		j = json.load(file)
	j[cur] = prefix
	with open('AltCoinVersionPrefixes', 'w') as file:
		json.dump(j, file)
	print('version prefix = ' + str((int(prefix, 16)-128)))
	return
	
if __name__ == "__main__":
	getPrivKey()
	
