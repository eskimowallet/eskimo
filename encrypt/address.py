def o_priv_wif_c(priv, version=0):
	return o_b58(encode(priv, 256, 32) + '\x01', (128+version))


def o_priv_to_pub(priv):
    """ integer 256 bit ECC private key to hexstring compressed public key
    """
    pub = base10_multiply(G, priv)
    return '0' + str(2 + (pub[1] % 2)) + encode(pub[0], 16, 64)


def o_pub_to_addr(pub, version=0):
    """ Compressed ECC public key hex to Bitcoin address
    """
    return o_b58(hashlib.new('ripemd160', hashlib.sha256(pub.decode('hex')).digest()).digest(), (0+version))


def o_b58(r160, magicbyte=0):
    """ Base58 encoding w leading zero compact
    """
    from re import match as re_match
    inp_fmtd = chr(int(magicbyte)) + r160
    leadingzbytes = len(re_match('^\x00*', inp_fmtd).group(0))
    checksum = hashlib.sha256(hashlib.sha256(inp_fmtd).digest()).digest()[:4]
    return 'L' * leadingzbytes + encode(decode(inp_fmtd + checksum, 256), 58, 0)


def sxor(s1, s2):
    """ XOR strings
    """
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))