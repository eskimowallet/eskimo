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
