def bip38(priv, passphrase, quiet=False):
    """
    BIP0038 private key encryption, Non-EC
    """
    prnt('\nCalculating encrypted private key...\n', quiet)
    addr = o_pub_to_addr(o_priv_to_pub(priv))
#1 Compute the Bitcoin address (ASCII), and take the first four bytes of SHA256(SHA256()) of it.
    addrhash = hashlib.sha256(hashlib.sha256(addr).digest()).digest()[:4]  # salt

#2. Derive a key from the passphrase using scrypt
#     a.  Parameters: passphrase is the passphrase itself encoded in UTF-8.
#         addresshash came from the earlier step, n=16384, r=8, p=8, length=64
#         (n, r, p are provisional and subject to consensus)
#     b. Let's split the resulting 64 bytes in half, and call them derivedhalf1 and derivedhalf2.
    # scrypt(password, salt, n, r, p, buflen):
    scryptedkey = scrypt(passphrase, addrhash, 16384, 8, 8, 64, quiet)
    half1 = scryptedkey[0:32]
    half2 = scryptedkey[32:64]

#3 AES encryptedhalf1 = AES256Encrypt(bitcoinprivkey[0...15] xor derivedhalf1[0...15], derivedhalf2)
    priv256 = encode(priv, 256, 32)
    aes4b38 = Aes(half2)  # set AES object key
    ehalf1 = aes4b38.enc(sxor(priv256[:16], half1[:16]))

#4 AES encryptedhalf2 =  AES256Encrypt(bitcoinprivkey[16...31] xor derivedhalf1[16...31], derivedhalf2)
    ehalf2 = aes4b38.enc(sxor(priv256[16:32], half1[16:32]))

#5 Base58 ( 0x01 0x42 + flagbyte + salt + encryptedhalf1 + encryptedhalf2 )
    fbyte = chr(0b11100000)  # 11 noec 1 compressedpub 00 future 0 ec only 00 future
    encrypted_privkey = ('\x01\x42' + fbyte + addrhash + ehalf1 + ehalf2)
    encrypted_check = hashlib.sha256(hashlib.sha256(encrypted_privkey).digest()).digest()[:4]
    return b58encode(encrypted_privkey + encrypted_check)
