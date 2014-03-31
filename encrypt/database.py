from hashlib import md5
import aes.aes as aes
import rand.rand as rand
import tools.db as db
import os

def derive_key_and_iv(password, salt, key_length, iv_length):
    d = d_i = ''
    while len(d) < key_length + iv_length:
        d_i = md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length+iv_length]

def encrypt(passW):
    print('encrypting database. please wait...')
    bs = 128
    inFile = 'igloo.dat'
    outFile = 'iceblock'
    if not os.path.isfile(inFile) and os.path.isfile(outFile):
        print('database is already encrypted')
        return
    salt = str(rand.clockrnd())[:(bs - len('Salted__'))]
    in_file = open('igloo.dat', 'rb')
    out_file = open('iceblock', 'wb')
    key, iv = derive_key_and_iv(passW, salt, 32, bs)
    out_file.write('Salted__' + salt)
    finished = False
    while not finished:
        chunk = in_file.read(1024 * bs)
        if len(chunk) == 0 or len(chunk) % bs != 0:
            padding_length = (bs - len(chunk) % bs) or bs
            chunk += padding_length * chr(padding_length)
            finished = True
        out_file.write(aes.encryptData(key, chunk))
    in_file.close()
    out_file.close()
    os.remove(inFile)
    return db.testEnc()

def decrypt(passW):
    print('decrypting database. please wait...')
    bs = 128
    inFile = 'iceblock'
    outFile = 'igloo.dat'
    if not os.path.isfile(inFile) and os.path.isfile(outFile):
        print('database is already encrypted')
        return
    in_file = open(inFile, 'rb')
    out_file = open(outFile, 'wb')
    salt = in_file.read(bs)[len('Salted__'):]
    key, iv = derive_key_and_iv(passW, salt, 32, bs)
    next_chunk = ''
    finished = False
    while not finished:
        chunk, next_chunk = next_chunk, aes.decryptData(key, in_file.read(1024 * bs))
        if len(next_chunk) == 0:
            padding_length = ord(chunk[-1])
            chunk = chunk[:-padding_length]
            finished = True
        out_file.write(chunk)
    in_file.close()
    out_file.close()
    os.remove(inFile)
    return db.testDec()
