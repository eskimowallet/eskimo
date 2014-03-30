from hashlib import md5
from Crypto.Cipher import AES
from Crypto import Random
import os
import sqlite3

def derive_key_and_iv(password, salt, key_length, iv_length):
    d = d_i = ''
    while len(d) < key_length + iv_length:
        d_i = md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length+iv_length]

def encrypt():
	in_file = open('igloo.dat', 'rb')
	out_file = open('iceblock', 'wb')
    	bs = AES.block_size
    	salt = Random.new().read(bs - len('Salted__'))
    	conn = sqlite3.connect('igloo.dat')
	c = conn.cursor()
	c.execute('select value from eskimo_settings where name=?;', ('encryption_passphrase',))
	passp = c.fetchone()
	conn.close()
	if passp is None:
		password = dbCreate.setPwd(1)
	else:
		password = passp[0]
    	key, iv = derive_key_and_iv(password, salt, 32, bs)
    	cipher = AES.new(key, AES.MODE_CBC, iv)
    	out_file.write('Salted__' + salt)
    	finished = False
    	while not finished:
    		chunk = in_file.read(1024 * bs)
        	if len(chunk) == 0 or len(chunk) % bs != 0:
            		padding_length = (bs - len(chunk) % bs) or bs
            		chunk += padding_length * chr(padding_length)
            		finished = True
        	out_file.write(cipher.encrypt(chunk))
        os.remove(in_file)

def decrypt():
	in_file = open('iceblock', 'rb')
	out_file = open('igloo.dat', 'wb')
	bs = AES.block_size
	salt = in_file.read(bs)[len('Salted__'):]
	password = raw_input('Enter password to decrypt database : ')
	key, iv = derive_key_and_iv(password, salt, 32, bs)
	cipher = AES.new(key, AES.MODE_CBC, iv)
	next_chunk = ''
	finished = False
	while not finished:
		chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
		if len(next_chunk) == 0:
			padding_length = ord(chunk[-1])
			chunk = chunk[:-padding_length]
			finished = True
		out_file.write(chunk)
    	os.remove(in_file)
