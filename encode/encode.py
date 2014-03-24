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
	
	
def b58encode(v):
    """ gavin bitcointool - encode v, which is a string of bytes, to base58.
    """
    _b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    _b58base = len(_b58chars)

    #(c style int->base256)
    long_value = 0L
    for (i, c) in enumerate(v[::-1]):
        long_value += (256**i) * ord(c)
    result = ''
    while long_value >= _b58base:
        div, mod = divmod(long_value, _b58base)
        result = _b58chars[mod] + result
        long_value = div
    result = _b58chars[long_value] + result
    zeropad = 0
    for c in v:
        if c == '\x00':
            zeropad += 1
        else:
            break
    return '1'*zeropad + result
	
def get_code_string(base):
    if base == 16:
        return "0123456789abcdef"
    elif base == 58:
        return "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    elif base == 256:
        return ''.join([chr(x) for x in range(256)])
    else:
        raise ValueError("Invalid base!")


def encode(val, base, minlen=0):
    code_string = get_code_string(base)
    result = ""
    while val > 0:
        result = code_string[val % base] + result
        val /= base
    if len(result) < minlen:
        result = code_string[0] * (minlen - len(result)) + result
    return result


def decode(string, base):
    code_string = get_code_string(base)
    result = 0
    if base == 16:
        string = string.lower()
    while len(string) > 0:
        result *= base
        result += code_string.find(string[0])
        string = string[1:]
    return result