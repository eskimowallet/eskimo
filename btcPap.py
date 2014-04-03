#!/usr/bin/env python
"""
Bitcoin paper wallet generator v1.2

This code, excepting the MIT-licensed libraries,
is public domain. Everyone has the right to do whatever they want
with it for any purpose.

Also MIT licensed, when needed for redistribution:

The MIT License (MIT)

Copyright (c) 2013 deepceleron of bitcointalk.org
pybitcointools Copyright (c) 2013 Vitalik Buterin
https://github.com/vbuterin/pybitcointools/

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""


# AES
# Copyright 2011 Alexey V Michurin <a.michurin@gmail.com>. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice, this list of
#       conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above copyright notice, this list
#       of conditions and the following disclaimer in the documentation and/or other materials
#       provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY Alexey V Michurin ''AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL Alexey V Michurin OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are those of the
# authors and should not be interpreted as representing official policies, either expressed
# or implied, of Alexey V Michurin.


KLEN_OPTIONS = {
    16: 10,
    24: 12,
    32: 14}

RCON = [  # http://en.wikipedia.org/wiki/Rijndael_key_schedule
    0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
    0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a,
    0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a,
    0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39,
    0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25,
    0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a,
    0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08,
    0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8,
    0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6,
    0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef,
    0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61,
    0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc,
    0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01,
    0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b,
    0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e,
    0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3,
    0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4,
    0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94,
    0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8,
    0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20,
    0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d,
    0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35,
    0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91,
    0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f,
    0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d,
    0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04,
    0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c,
    0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63,
    0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa,
    0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd,
    0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66,
    0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d]

SBOX = [  # http://en.wikipedia.org/wiki/Rijndael_S-box
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5,
    0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0,
    0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc,
    0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a,
    0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0,
    0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b,
    0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85,
    0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5,
    0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17,
    0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88,
    0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c,
    0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9,
    0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6,
    0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e,
    0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94,
    0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68,
    0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]

INVSBOX = [
    0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38,
    0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
    0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87,
    0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
    0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d,
    0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
    0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2,
    0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
    0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16,
    0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
    0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda,
    0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
    0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a,
    0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
    0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02,
    0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
    0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea,
    0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
    0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85,
    0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
    0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89,
    0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
    0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20,
    0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
    0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31,
    0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
    0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d,
    0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
    0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0,
    0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26,
    0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d]


def xor_words(a, b):
    return map(lambda x: x[0] ^ x[1], zip(a, b))


def expand_key(zkey):
    klen = len(zkey)
    nr = KLEN_OPTIONS[klen]
    ekdlen = 16 * (nr + 1)  # 16 = 4 * Nb, Nb = 4
    ekey = zkey[:]
    eklen = klen
    rcon_iter = 0
    while eklen < ekdlen:
        temp = ekey[-4:]
        if eklen % klen == 0:
            # rotate
            temp = temp[1:] + temp[:1]
            # sub word
            for i in xrange(4):
                temp[i] = SBOX[temp[i]]
            # xor w rcon
            rcon_iter += 1   # incremet first, RCON starts from 1
            temp[0] ^= RCON[rcon_iter]
        if klen == 32 and eklen % 32 == 16:
            for i in xrange(4):
                temp[i] = SBOX[temp[i]]
        for t in temp:
            ekey.append(ekey[-klen] ^ t)
            eklen += 1
    return ekey, nr


def gm(a, b):  # Galois multiplication of 8 bit characters a and b.
    p = 0
    for _ in xrange(8):
        if b & 1:
            p ^= a
        a <<= 1
        if a & 0x100:
            a ^= 0x1b
        b >>= 1
    return p & 0xff


def mix_col(col, mul):
    r = []
    for i in xrange(4):
        t = 0
        for j in xrange(4):
            t ^= gm(col[(i+4-j) % 4], mul[j])
        r.append(t)
    return r


def mix_cols(st, mul):
    for s in xrange(0, 16, 4):
        p = s + 4
        st[s:p] = mix_col(st[s:p], mul)
    return st


def sub_bytes(st, sbox):
    for i in xrange(16):
        st[i] = sbox[st[i]]
    return st


def shift_rows(st):
    for r in xrange(1, 4):
        s = r * 5      # s = r + r * 4
        st[r:16:4] = st[s:16:4] + st[r:s:4]
    return st


def inv_shift_rows(st):
    for r in xrange(1, 4):
        s = 16 - 3 * r  # r + 16 - 4 * r
        st[r:16:4] = st[s:16:4] + st[r:s:4]
    return st


def encryption_loop(etext, ekey, nr):
    nr16 = nr * 16
    state = xor_words(etext, ekey[:16])  # add round key
    for eks in xrange(16, nr16, 16):
        state = sub_bytes(state, SBOX)
        state = shift_rows(state)
        state = mix_cols(state, (2, 1, 1, 3))
        state = xor_words(state, ekey[eks:eks+16])  # add round key
    state = sub_bytes(state, SBOX)
    state = shift_rows(state)
    state = xor_words(state, ekey[nr16:nr16 + 16])  # add round key
    return state


def decryption_loop(dcryp, ekey, nr):
    nr16 = nr * 16
    state = xor_words(dcryp, ekey[nr16:nr16 + 16])  # add round key
    for eks in xrange(nr16, 31, -16):
        state = inv_shift_rows(state)
        state = sub_bytes(state, INVSBOX)
        state = xor_words(state, ekey[eks-16:eks])  # add round key
        state = mix_cols(state, (14, 9, 13, 11))
    state = inv_shift_rows(state)
    state = sub_bytes(state, INVSBOX)
    state = xor_words(state, ekey[:16])  # add round key
    return state


def encrypt(etext, zkey):
    ekey, nr = expand_key(zkey)
    return encryption_loop(etext, ekey, nr)


def decrypt(ecryp, zkey):
    ekey, nr = expand_key(zkey)
    return decryption_loop(ecryp, ekey, nr)


def str_to_vec(x):
    return list(map(ord, x))


def vec_to_str(x):
    return ''.join(map(chr, x))


class Aes:

    def __init__(self, key):
        self.ekey, self.nr = expand_key(str_to_vec(key))

    def enc(self, text):
        return vec_to_str(encryption_loop(str_to_vec(text), self.ekey, self.nr))

    def dec(self, cryp):
        return vec_to_str(decryption_loop(str_to_vec(cryp), self.ekey, self.nr))


# pbkdf2/scrypt
# Copyright (c) 2011 Allan Saddi <allan@saddi.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

import hashlib
import hmac
import struct

DEFAULT_DIGESTMOD = hashlib.sha1


def f(password, salt, itercount, i, digestmod):
    u = hmac.new(password, salt + struct.pack('>i', i), digestmod).digest()
    result = [ord(x) for x in u]
    for j in range(1, itercount):
        u = hmac.new(password, u, digestmod).digest()
        u_result = [ord(x) for x in u]
        for x in range(len(u_result)):
            result[x] ^= u_result[x]
    return ''.join([chr(x) for x in result])


def pbkdf(password, salt, itercount, dklen, digestmod=DEFAULT_DIGESTMOD, digest_size=None):
    if digest_size is None:
        digest_size = digestmod().digest_size
    if dklen > (2**32-1) * digest_size:
        raise ValueError('derived key too long')
    l = (dklen + digest_size - 1) / digest_size
    dk = []
    for i in range(1, l+1):
        dk.append(f(password, salt, itercount, i, digestmod))
    return ''.join(dk)[:dklen]


# Scrypt

from itertools import izip
MASK32 = 2**32-1
BLOCK_WORDS = 16


def rotl(n, r):
    return ((n << r) & MASK32) | ((n & MASK32) >> (32 - r))


def doubleround(x):
    x[4] ^= rotl(x[0]+x[12], 7)
    x[8] ^= rotl(x[4]+x[0], 9)
    x[12] ^= rotl(x[8]+x[4], 13)
    x[0] ^= rotl(x[12]+x[8], 18)
    x[9] ^= rotl(x[5]+x[1], 7)
    x[13] ^= rotl(x[9]+x[5], 9)
    x[1] ^= rotl(x[13]+x[9], 13)
    x[5] ^= rotl(x[1]+x[13], 18)
    x[14] ^= rotl(x[10]+x[6], 7)
    x[2] ^= rotl(x[14]+x[10], 9)
    x[6] ^= rotl(x[2]+x[14], 13)
    x[10] ^= rotl(x[6]+x[2], 18)
    x[3] ^= rotl(x[15]+x[11], 7)
    x[7] ^= rotl(x[3]+x[15], 9)
    x[11] ^= rotl(x[7]+x[3], 13)
    x[15] ^= rotl(x[11]+x[7], 18)
    x[1] ^= rotl(x[0]+x[3], 7)
    x[2] ^= rotl(x[1]+x[0], 9)
    x[3] ^= rotl(x[2]+x[1], 13)
    x[0] ^= rotl(x[3]+x[2], 18)
    x[6] ^= rotl(x[5]+x[4], 7)
    x[7] ^= rotl(x[6]+x[5], 9)
    x[4] ^= rotl(x[7]+x[6], 13)
    x[5] ^= rotl(x[4]+x[7], 18)
    x[11] ^= rotl(x[10]+x[9], 7)
    x[8] ^= rotl(x[11]+x[10], 9)
    x[9] ^= rotl(x[8]+x[11], 13)
    x[10] ^= rotl(x[9]+x[8], 18)
    x[12] ^= rotl(x[15]+x[14], 7)
    x[13] ^= rotl(x[12]+x[15], 9)
    x[14] ^= rotl(x[13]+x[12], 13)
    x[15] ^= rotl(x[14]+x[13], 18)


def salsa20_8_core(x):
    z = list(x)
    for i in range(4):
        doubleround(z)
    for i in range(16):
        z[i] = (z[i] + x[i]) & MASK32
    return z


def blockmix_salsa20_8(b, r=8):
    y = [None]*(2 * r * BLOCK_WORDS)
    even = 0
    odd = r * BLOCK_WORDS
    t = b[(2 * r - 1) * BLOCK_WORDS:]

    for i in range(0, 2 * r * BLOCK_WORDS, 2 * BLOCK_WORDS):
        for j in range(BLOCK_WORDS):
            t[j] ^= b[i + j]
        y[even:even+BLOCK_WORDS] = t = salsa20_8_core(t)
        even += BLOCK_WORDS

        for j in range(BLOCK_WORDS):
            t[j] ^= b[i + BLOCK_WORDS + j]
        y[odd:odd+BLOCK_WORDS] = t = salsa20_8_core(t)
        odd += BLOCK_WORDS
    return y


def from_littleendian(b):
    return ord(b[0]) | (ord(b[1]) << 8) | (ord(b[2]) << 16) | (ord(b[3]) << 24)


def to_littleendian(w):
    return [chr(w & 0xff),
            chr((w >> 8) & 0xff),
            chr((w >> 16) & 0xff),
            chr((w >> 24) & 0xff)]


def smix(b, n, r=8):
    x = [from_littleendian(b[i:i+4]) for i in range(0, len(b), 4)]
    v = []
    for i in range(n):
        v.append(x)
        x = blockmix_salsa20_8(x, r=r)
    for i in range(n):
        j = x[-BLOCK_WORDS] % n

        t = []
        for xk, vjk in izip(x, v[j]):
            t.append(xk ^ vjk)
        x = blockmix_salsa20_8(t, r=r)
    out = []
    for x in x:
        out.extend(to_littleendian(x))
    return ''.join(out)


def scrypt(password, salt, n, r, p, buflen=64, quiet=False):
    mflen = 2 * r * 4 * BLOCK_WORDS
    t = pbkdf(password, salt, 1, p * mflen, digestmod=hashlib.sha256)
    b = []

    while t:
        b.append(t[:mflen])
        t = t[mflen:]

    for i in range(p):
        prnt('stage ' + str(i+1) + ' of ' + str(p) + '...\n', quiet)
        b[i] = smix(b[i], n, r=r)
    return pbkdf(password, ''.join(b), 1, buflen, digestmod=hashlib.sha256)


### Elliptic curve math - pybitcointools

#P = 2 ** 256 - 2 ** 32 - 2 ** 9 - 2 ** 8 - 2 ** 7 - 2 ** 6 - 2 ** 4 - 1
P = 115792089237316195423570985008687907853269984665640564039457584007908834671663
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337
A = 0
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
G = (Gx, Gy)


def inv(a, n):
    lm, hm = 1, 0
    low, high = a % n, n
    while low > 1:
        r = high / low
        nm, new = hm - lm * r, high - low * r
        lm, low, hm, high = nm, new, lm, low
    return lm % n


def isinf(p):
    return p[0] == 0 and p[1] == 0


def base10_add(a, b):
    if isinf(a):
        return b[0], b[1]
    if isinf(b):
        return a[0], a[1]
    if a[0] == b[0]:
        if a[1] == b[1]:
            return base10_double((a[0], a[1]))
        else:
            return 0, 0
    m = ((b[1] - a[1]) * inv(b[0] - a[0], P)) % P
    x = (m * m - a[0] - b[0]) % P
    y = (m * (a[0] - x) - a[1]) % P
    return x, y


def base10_double(a):
    if isinf(a):
        return 0, 0
    m = ((3 * a[0] * a[0] + A) * inv(2 * a[1], P)) % P
    x = (m * m - 2 * a[0]) % P
    y = (m * (a[0] - x) - a[1]) % P
    return x, y


def base10_multiply(a, n):
    if isinf(a) or n == 0:
        return 0, 0
    if n == 1:
        return a
    if n < 0 or n >= N:
        return base10_multiply(a, n % N)
    if (n % 2) == 0:
        return base10_double(base10_multiply(a, n / 2))
    if (n % 2) == 1:
        return base10_add(base10_double(base10_multiply(a, n / 2)), a)


# Address encoding

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


# Bitcoin compressed address only


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


# Bitcoin compressed address only - (todo: rewrite due to b58 incompatible with BIP38)

def o_priv_wif_c(priv):
        return o_b58(encode(priv, 256, 32) + '\x01', 128)


def o_priv_to_pub(priv):
    """ integer 256 bit ECC private key to hexstring compressed public key
    """
    pub = base10_multiply(G, priv)
    return '0' + str(2 + (pub[1] % 2)) + encode(pub[0], 16, 64)


def o_pub_to_addr(pub):
    """ Compressed ECC public key hex to Bitcoin address
    """
    return o_b58(hashlib.new('ripemd160', hashlib.sha256(pub.decode('hex')).digest()).digest(), 0)


def o_b58(r160, magicbyte=0):
    """ Base58 encoding w leading zero compact
    """
    from re import match as re_match
    inp_fmtd = chr(int(magicbyte)) + r160
    leadingzbytes = len(re_match('^\x00*', inp_fmtd).group(0))
    checksum = hashlib.sha256(hashlib.sha256(inp_fmtd).digest()).digest()[:4]
    return '1' * leadingzbytes + encode(decode(inp_fmtd + checksum, 256), 58, 0)


def sxor(s1, s2):
    """ XOR strings
    """
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))


def bip38(priv, passphrase, quiet=False):
	"""
	BIP0038 private key encryption, Non-EC
	"""
	prnt('\nCalculating encrypted private key...\n', quiet)
	addr = o_pub_to_addr(o_priv_to_pub(priv))
	#1 Compute the Bitcoin address (ASCII), and take the first four bytes of SHA256(SHA256()) of it.
	addrhash = hashlib.sha256(hashlib.sha256(addr).digest()).digest()[:4]  # salt
	print('addresshash = ' + addrhash)
	#2. Derive a key from the passphrase using scrypt
	#     a.  Parameters: passphrase is the passphrase itself encoded in UTF-8.
	#         addresshash came from the earlier step, n=16384, r=8, p=8, length=64
	#         (n, r, p are provisional and subject to consensus)
	#     b. Let's split the resulting 64 bytes in half, and call them derivedhalf1 and derivedhalf2.
	# scrypt(password, salt, n, r, p, buflen):
	scryptedkey = scrypt(passphrase, addrhash, 16384, 8, 8, 64, quiet)
	print('key = ' + str(scryptedkey))
	half1 = scryptedkey[0:32]
	half2 = scryptedkey[32:64]

	print('derivedhalf1 = ' + str(half1))
	print('derivedhalf2 = ' + str(half2))

	#3 AES encryptedhalf1 = AES256Encrypt(bitcoinprivkey[0...15] xor derivedhalf1[0...15], derivedhalf2)
	priv256 = encode(priv, 256, 32)
	aes4b38 = Aes(half2)  # set AES object key
	ehalf1 = aes4b38.enc(sxor(priv256[:16], half1[:16]))
	print('privK = ' + str(priv256))
	print('encryptedhalf1 = ' + str(ehalf1))

	#4 AES encryptedhalf2 =  AES256Encrypt(bitcoinprivkey[16...31] xor derivedhalf1[16...31], derivedhalf2)
	ehalf2 = aes4b38.enc(sxor(priv256[16:32], half1[16:32]))
	print('encryptedhalf2 = ' + str(ehalf2))
	#5 Base58 ( 0x01 0x42 + flagbyte + salt + encryptedhalf1 + encryptedhalf2 )
	fbyte = chr(0b11100000)  # 11 noec 1 compressedpub 00 future 0 ec only 00 future
	encrypted_privkey = ('\x01\x42' + fbyte + addrhash + ehalf1 + ehalf2)
	print('encPrivK = ' + str(encrypted_privkey))
	encrypted_check = hashlib.sha256(hashlib.sha256(encrypted_privkey).digest()).digest()[:4]
	print('check = ' + str(encrypted_check))
	b58 = b58encode(encrypted_privkey + encrypted_check)
	print('b58 = ' + str(b58))
	return b58


class _Getch:
    """
    Gets a single character from standard input.  Does not echo to the screen.
    """
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            try:
                self.impl = _GetchMacCarbon()
            except(AttributeError, ImportError):
                self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty
        import sys
        import termios  # import termios now or else you'll get the Unix version on the Mac

    def __call__(self):
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        akey = msvcrt.getch()
        if akey == '\xe0' or akey == '\000':
            raise KeyboardInterrupt('break for ctrl-tab and others')
        return akey


class _GetchMacCarbon:
    """
    A function which returns the current ASCII key that is down;
    if no ASCII key is down, the null string is returned.
    """
    def __init__(self):
        import Carbon
        test = Carbon.Evt  # see if it has this (in Unix, it doesn't)

    def __call__(self):
        import Carbon
        if Carbon.Evt.EventAvail(0x0008)[0] == 0:  # 0x0008 is the keyDownMask
            return ''
        else:
            (what, msg, when, where, mod) = Carbon.Evt.GetNextEvent(0x0008)[1]
            return chr(msg & 0x000000FF)

from sys import stdout


def clockbase():
    """
    256 bit hex: 4 x 16 byte long from float using clock (process time) + time (UTC epoch time)
    Note: not enough clock precision on Linuxes to be unique between two immediate calls
    """
    from struct import pack
    from time import time, clock

    return pack('<dddd', clock(), time(), clock(), time()).encode('hex')


def clockrnd():
    """
    512 bit int: random delay while hashing data,
    return result of 192-1725 time-based hashes.
    execution time on 2.8GHz Core2: 1.8-15.7ms
    """
    loopcount = 64 + int(hashlib.sha256(clockbase()).hexdigest()[:3], 16)/8  # 64-575 loops, random
    hash1 = hash2 = int(clockbase()+clockbase(), 16)
    for i in xrange(loopcount):
        hash1 ^= int(hashlib.sha512(clockbase() + hashlib.sha512(clockbase()).hexdigest()).hexdigest(), 16)
        hash2 ^= int(hashlib.sha512((hex(hash1)) + ('%d' % hash1)).hexdigest(), 16)
    return hash1 ^ hash2


def platform_check(checks=50, quiet=False):
    from collections import Counter
    if checks > 100 and not quiet:
        prnt('** Running platform validation tests **\n', quiet)
    l = []
    for zbit in xrange(checks):
        l.append(clockrnd())
    r = Counter(l).most_common(1)
    x, count = r[0]
    if count != 1:
        raise Exception('FAIL: time-based entropy not always unique!')
    if checks > 100 and not quiet:
        prnt('...pass\n', quiet)
    return True


def keyboard_entropy(keynum=32, quiet=False):
    """
    512 bit random number from keyboard and keypress timer
    """

    keypress = _Getch()
    typed = kr = 'Press keys to generate secure address........'
    hashes = clockrnd()
    prnt(kr, quiet)
    for step in range(keynum, 0, -1):
        for cnt in xrange(10000000):  # only loops on OSX
            hashes ^= clockrnd()
            kr = keypress()
            if kr != '':
                break
        typed += kr
        hashes ^= clockrnd()
        prnt('\b\b\b\b{0:4d}'.format(step-1), quiet)
    prnt('\b\b\b\b  OK\n', quiet)
    return hashes ^ int(hashlib.sha512(typed*8).hexdigest(), 16)


def keyboard_passphrase(turn=0, quiet=False):  # this can't really be "quiet"
    progress_step = 0
    pretty_progress = ['\b*', '\bo', '\bO']
    keypress = _Getch()
    single_key = passw = ''
    msg = ' Enter your wallet passphrase (will not appear)......'
    if turn != 0:
        msg = ' Re-enter to verify your wallet passphrase......'
    prnt(msg)

    while single_key != "\n" and single_key != chr(13):
        while True:
            single_key = keypress()
            if single_key != '':
                break
        #print ord(single_key)
        if single_key != "\n" and single_key != chr(13):
            passw += single_key
        prnt(pretty_progress[progress_step % 3], quiet)
        progress_step += 1
    prnt('\b\n', quiet)
    return passw


def prnt(printstring, silent=False):
    """
    STDOUT console printing with an option to disable
    """
    if not silent:
        stdout.write(printstring)


def random_key(entropy):
    """
    256 bit number from equally strong urandom, user entropy, and timer parts
    """
    if entropy.bit_length() < 250:
        raise Exception('Insufficent entropy parameter to generate key')
    from random import SystemRandom
    osrndi = SystemRandom()
    entstr = encode(entropy, 16) + encode(osrndi.getrandbits(512), 256) + str(clockrnd())
    osrnd = SystemRandom(entstr)
    privkey = 0
    while privkey < 1 or privkey > N:
        privkey = decode(hashlib.sha256(encode(osrnd.getrandbits(512), 256)).digest(), 256) ^ osrnd.getrandbits(256)
        for lbit in xrange(clockrnd() % 64 + 64):
            clockstr = hex(clockrnd()) + str(clockrnd()) + entstr
            # Confused? These slice a moving 256 bit window out of SHA512
            clock32 = hashlib.sha512(clockstr).digest()[1+(lbit % 29): 33+(lbit % 29)]
            randhash = hashlib.sha512(encode(osrnd.getrandbits(512), 256)).digest()[0+(lbit % 31): 32+(lbit % 31)]
            privkey ^= decode(randhash, 256) ^ decode(clock32, 256) ^ osrndi.getrandbits(256)
            osrnd = SystemRandom(hashlib.sha512(clock32 + randhash + entstr).digest())  # reseed
    return privkey


# This is the real program, all that other stuff was just a clever ploy to distract you ;)
from optparse import OptionParser, OptionGroup


def paperwal():
    parser = OptionParser()
    parser.add_option("-e", "--encrypted", action='store_true', dest="encrypted", default=False,
                      help="create BIP38-encrypted privkey (takes a LONG time)")
    parser.add_option("-v", "--validate", action='store_true', dest="validate", default=False,
                      help="enable extensive system tests for entropy")
    parser.add_option("-s", "--silent", action='store_true', dest="silent", default=False,
                      help="disable most console output except address")
    parser.add_option("-l", "--loop", action='store_true', dest="repeat", default=False,
                      help="restart instead of exit")
    parser.add_option("-p", "--nopause", action='store_true', dest="nopause", default=False,
                      help="disable the pause before exiting")
    parser.add_option("-d", "--doublecalc", action='store_true', dest="doublecalc", default=False,
                      help="calculate twice and test results")
    parser.add_option("-z", "", dest='just a helpful hint', default='',
                      help="try ctrl-tab to abort the program")
    entropy_warning = OptionGroup(parser, "Warning",
                                          "If you use this option, you should supply REAL randomly generated entropy. "
                                          "It is probably a good idea not to reuse a seed.")
    entropy_warning.add_option("-r", "--entropy", dest='entropy', default='',
                               help="random seed instead of keypresses, 64+ characters")
    parser.add_option_group(entropy_warning)
    (options, args) = parser.parse_args()

    if options.doublecalc:
        calcs = 2
    else:
        calcs = 1

    if options.entropy and len(options.entropy) < 64:
        prnt('\n** User-supplied seed too short, using keypresses instead\n')
    if options.validate:
        check_rounds = 1000
    else:
        check_rounds = 50
    platform_check(check_rounds)
    runcount = 0

    while runcount < 1 or options.repeat:
        bip38pass1 = showpass = ''
        bip38pass2 = 'not equal'

        if options.encrypted:
            while bip38pass1 != bip38pass2 or len(bip38pass1) < 1:
                bip38pass1 = keyboard_passphrase()
                bip38pass2 = keyboard_passphrase(2)
                if bip38pass1 != bip38pass2:
                    prnt('\n** The passphrase entered did not match!\n')
                elif len(bip38pass1) < 1:
                    prnt('\n** No passphrase was entered!\n')

            prnt('\n Show your passphrase before continuing? (y/n)\n')
            getkey = _Getch()
            while True:
                showpass = getkey()
                if showpass != '':
                    break
            if showpass.lower() == 'y' and not options.silent:
                prnt('   Passphrase: (' + bip38pass1 + ')\n')
                pwcounter = '1234567890123456789012345678901234567890'[:len(bip38pass1)]
                prnt('    (counter):  ' + pwcounter + '\n\n')

        if len(options.entropy) > 63:
            userentropy = int(options.entropy.encode('hex'), 16)
        else:
            userentropy = keyboard_entropy(quiet=options.silent)

        privk = 40131568902706951395453712757810642216863964538517508976269348707743442884300 #random_key(userentropy)
        wallettest = ['', '']
        for loop in xrange(calcs):
            privc = o_priv_wif_c(privk)
            #priv_wif_c = o_b58(encode(privk, 256, 32) + '\x01', ord('\x80'))
            pubc = o_priv_to_pub(privk)
            paper_address = 'Bitcoin Address:\n ' + o_pub_to_addr(pubc) + '\n'

            if not options.encrypted:
                paper_address += 'Private Key:\n ' + privc + '\n'
            else:
                priv_enc = bip38(privk, bip38pass1, options.silent)
                #priv_enc = 'FakePrivateEncryptedKey'  # debugging without waiting 15 minutes
                paper_address += 'Encrypted Private Key:\n ' + priv_enc + '\n'

            wallettest[loop] = paper_address
            # wallettest[1] += 'junk'  # debug - simulate calcuation failure
            if loop > 0:
                if wallettest[loop] != wallettest[loop-1]:
                    print("### CALCULATION FAILURE DETECTED - DO NOT USE ###")
                    prnt("### CALCULATION FAILURE DETECTED - DO NOT USE ###\n")
            else:
                prnt('\n' + paper_address + '\n')
        runcount += 1

    if not options.nopause:
        raw_input('Press "Enter" to close')

if __name__ == "__main__":
    paperwal()
