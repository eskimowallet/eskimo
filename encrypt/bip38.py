from encrypt import address
from scrypt import scrypt
from aes import aes
from encode import enc
from input import inp
import sqlite3
from rand import rand
import hashlib
import binascii

def bip38_encrypt(priv, passphrase, version=0, prefix=1):
	"""
    	BIP0038 private key encryption, Non-EC
    	"""
	print('Calculating encrypted private key...')
    
	#1 Compute the Bitcoin address (ASCII), and take the first four bytes of SHA256(SHA256()) of it.
	addr = address.publicKey2Address(address.privateKey2PublicKey(priv), version, prefix)
	addrhash = hashlib.sha256(hashlib.sha256(addr).digest()).digest()[:4]  # salt

	#2. Derive a key from the passphrase using scrypt
	#     a.  Parameters: passphrase is the passphrase itself encoded in UTF-8.
	#         addresshash came from the earlier step, n=16384, r=8, p=8, length=64
	#         (n, r, p are provisional and subject to consensus)
	#     b. Let's split the resulting 64 bytes in half, and call them derivedhalf1 and derivedhalf2.
	    # scrypt(password, salt, n, r, p, buflen):
	scryptedkey = scrypt.scrypt(passphrase, addrhash, 16384, 8, 8, 64)
	half1 = scryptedkey[0:32]
	half2 = scryptedkey[32:64]

	#3 AES encryptedhalf1 = AES256Encrypt(bitcoinprivkey[0...15] xor derivedhalf1[0...15], derivedhalf2)
	priv256 = enc.encode(priv, 256, 32)
	aes4b38 = aes.Aes(half2)  # set AES object key
	ehalf1 = aes4b38.enc(enc.sxor(priv256[:16], half1[:16]))

	#4 AES encryptedhalf2 =  AES256Encrypt(bitcoinprivkey[16...31] xor derivedhalf1[16...31], derivedhalf2)
	ehalf2 = aes4b38.enc(enc.sxor(priv256[16:32], half1[16:32]))

	#5 Base58 ( 0x01 0x42 + flagbyte + salt + encryptedhalf1 + encryptedhalf2 )
	fbyte = chr(0b11100000)  # 11 noec 1 compressedpub 00 future 0 ec only 00 future
	encrypted_privkey = ('\x01\x42' + fbyte + addrhash + ehalf1 + ehalf2)
	encrypted_check = hashlib.sha256(hashlib.sha256(encrypted_privkey).digest()).digest()[:4]
	return enc.b58encode(encrypted_privkey + encrypted_check)
	
def bip38_decrypt(encrypted_privkey,passphrase):
        '''
        BIP0038 non-ec-multiply decryption. Returns hex privkey.
        '''
        d = base58.b58decode(encrypted_privkey)
        d = d[2:]
        flagbyte = d[0:1]
        d = d[1:]
        # respect flagbyte, return correct pair
        if flagbyte == '\xc0':
            compressed = False
        if flagbyte == '\xe0':
            compressed = True
        print('compressed = ' + compressed)
        addresshash = d[0:4]
        d = d[4:-4]
        key = scrypt.scrypt(passphrase,addresshash, 16384, 8, 8)
        derivedhalf1 = key[0:32]
        derivedhalf2 = key[32:64]
        encryptedhalf1 = d[0:16]
        encryptedhalf2 = d[16:32]
        aes = aes.AES(derivedhalf2)
        decryptedhalf2 = aes.decrypt(encryptedhalf2)
        decryptedhalf1 = aes.decrypt(encryptedhalf1)
        priv = decryptedhalf1 + decryptedhalf2
        priv = binascii.unhexlify('%064x' % (long(binascii.hexlify(priv), 16) ^ long(binascii.hexlify(derivedhalf1), 16)))
        pub = address.privateKey2PublicKey(priv)
        if compressed:
            pub = encode_pubkey(pub,'hex_compressed')
        addr = address.publicKey2Address(pub)
        if hashlib.sha256(hashlib.sha256(addr).digest()).digest()[0:4] != addresshash:
            print('Addresshash Error')
            # TODO: investigate
            #self.decrypt_priv(wx.PostEvent) # start over
        else:
            return priv
	
def generate():
	print('creation of a BIP38 encrypted private key can take a long time (~15 minutes)')
	cont = raw_input('Do you want to continue? ').lower().strip()
	if not cont == 'y':
		return
	cur = raw_input('Enter currency abbreviation : ').upper().strip()
	if cur == '':
		return
	conn = sqlite3.connect('igloo.dat')
	c = conn.cursor()
	c.execute('select v.version,v.prefix,v.length,c.id,c.longName from eskimo_versions as v inner join eskimo_currencies as c on c.version = v.id where c.currency=?;', (cur.upper(),))
	version = c.fetchone()
	if version is None:
		print(cur.upper() + ' is not currently listed as a currency')
		return False
	bip38pass1 = 'bip38pass1' 
	bip38pass2 = 'bip38pass2'
	while bip38pass1 != bip38pass2 or len(bip38pass1) < 1:
		bip38pass1 = inp.keyboard_passphrase()
		bip38pass2 = inp.keyboard_passphrase(2)
		if bip38pass1 != bip38pass2:
		    print('The passphrases entered did not match!')
		elif len(bip38pass1) < 1:
		    print('No passphrase was entered!')
	privateKey = rand.randomKey(inp.keyboardEntropy())
	publicKey = address.privateKey2PublicKey(privateKey)
	publicAddress = address.publicKey2Address(publicKey, version[0], version[1])
	bipK = bip38_encrypt(privateKey, bip38pass1, version[0], version[1])
	
	c.execute('insert into eskimo_privK (privK, currency, bip) values (?,?,?);', (str(bipK).encode('base64','strict', str(True)), version[3]))
	privKid = c.lastrowid
	c.execute('insert into eskimo_addresses (address, currency) values (?,?);', (publicAddress.encode('base64','strict'), version[3]))
	addId = c.lastrowid
	c.execute('insert into eskimo_master(address, privK) values (?,?);', (addId, privKid))
	conn.commit()
	conn.close()
	print('')
	print(version[4] + ' Address : ' + publicAddress)
	#uncomment out the line below to show the BIP38 private key upon creation
	#print(str(bipK))
