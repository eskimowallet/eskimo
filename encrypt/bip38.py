import binascii
import hashlib
import sqlite3

import encrypt.aes as aes
import encrypt.scrypt as scrypt
import io.inp as inp
import num.enc as enc
import num.rand as rand


def encrypt(priv, addr, passphrase, version=0, prefix=1):
	'''
		BIP0038 private key encryption, Non-EC
	'''
	
	print('calculating BIP0038 encrypted private key...')
	
	#1 Take the first four bytes of SHA256(SHA256()) of the public address.
	addrhash = hashlib.sha256(hashlib.sha256(addr).digest()).digest()[:4]  # salt

	#2. Derive a key from the passphrase using scrypt
	#	 a.  Parameters: passphrase is the passphrase itself encoded in UTF-8.
	#		 addresshash came from the earlier step, n=16384, r=8, p=8, length=64
	#		 (n, r, p are provisional and subject to consensus)
	#	 b. Let's split the resulting 64 bytes in half, and call them derivedhalf1 and derivedhalf2.
		# scrypt(password, salt, n, r, p, buflen):
	scryptedkey = scrypt.scrypt(passphrase, addrhash, 16384, 8, 8, 64)
	half1 = scryptedkey[0:32]
	half2 = scryptedkey[32:64]

	#3 AES encryptedhalf1 = AES256Encrypt(bitcoinprivkey[0...15] xor derivedhalf1[0...15], derivedhalf2)
	priv256 = enc.encode(priv, 256, 32)
	ehalf1 = aes.encryptData(half2, enc.sxor(priv256[:16], half1[:16]))

	#4 AES encryptedhalf2 =  AES256Encrypt(bitcoinprivkey[16...31] xor derivedhalf1[16...31], derivedhalf2)
	ehalf2 = aes.encryptData(half2, enc.sxor(priv256[16:32], half1[16:32]))

	#5 Base58 ( 0x01 0x42 + flagbyte + salt + encryptedhalf1 + encryptedhalf2 )
	fbyte = chr(0b11100000)  # 11 noec 1 compressedpub 00 future 0 ec only 00 future
	encrypted_privkey = ('\x01\x42' + fbyte + addrhash + ehalf1 + ehalf2)
	encrypted_check = hashlib.sha256(hashlib.sha256(encrypted_privkey).digest()).digest()[:4]
	return enc.b58encode(encrypted_privkey + encrypted_check)
	
def decrypt(encrypted_privkey,passphrase):
		'''
		BIP0038 non-ec-multiply decryption. Returns hex privkey.
		'''
		d = str(enc.decode(encrypted_privkey, 58))
		d = d[2:]
		flagbyte = d[0:1]
		d = d[1:]
		# respect flagbyte, return correct pair
		if flagbyte == '\xc0':
			compressed = False
		if flagbyte == '\xe0':
			compressed = True
		addresshash = d[0:4]
		d = d[4:-4]
		key = scrypt.scrypt(passphrase,addresshash, 16384, 8, 8)
		derivedhalf1 = key[0:32]
		derivedhalf2 = key[32:64]
		encryptedhalf1 = d[0:16]
		encryptedhalf2 = d[16:32]
		decryptedhalf2 = aes.decryptData(derivedhalf2, encryptedhalf2)
		decryptedhalf1 = aes.decryptData(derivedhalf2, encryptedhalf1)
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
			
