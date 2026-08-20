from __future__ import annotations
import hashlib

B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
BECH32 = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"


def sha256(b: bytes) -> bytes: return hashlib.sha256(b).digest()
def dsha256(b: bytes) -> bytes: return sha256(sha256(b))
def ripemd160(b: bytes) -> bytes:
    h = hashlib.new('ripemd160'); h.update(b); return h.digest()
def hash160(b: bytes) -> bytes: return ripemd160(sha256(b))


def b58encode(raw: bytes) -> str:
    n = int.from_bytes(raw, 'big')
    out = ''
    while n:
        n, r = divmod(n,58); out = B58[r] + out
    z = len(raw) - len(raw.lstrip(b'\0'))
    return '1'*z + (out or ('' if z else '1'))


def b58decode(s: str) -> bytes:
    n=0
    for c in s:
        i=B58.find(c)
        if i<0: raise ValueError(f"invalid Base58 character: {c}")
        n=n*58+i
    body = n.to_bytes((n.bit_length()+7)//8, 'big') if n else b''
    z = len(s)-len(s.lstrip('1'))
    return b'\0'*z + body


def b58check_encode(payload: bytes) -> str:
    return b58encode(payload + dsha256(payload)[:4])


def b58check_decode(s: str) -> bytes:
    raw=b58decode(s)
    if len(raw)<5: raise ValueError('Base58Check value too short')
    payload,check=raw[:-4],raw[-4:]
    if dsha256(payload)[:4] != check: raise ValueError('Base58Check checksum mismatch')
    return payload


def _polymod(values):
    gens=(0x3b6a57b2,0x26508e6d,0x1ea119fa,0x3d4233dd,0x2a1462b3)
    chk=1
    for v in values:
        top=chk>>25; chk=(chk&0x1ffffff)<<5 ^ v
        for i,g in enumerate(gens):
            if (top>>i)&1: chk ^= g
    return chk

def _hrp_expand(hrp): return [ord(x)>>5 for x in hrp]+[0]+[ord(x)&31 for x in hrp]
def _convertbits(data, frombits, tobits, pad=True):
    acc=0; bits=0; out=[]; maxv=(1<<tobits)-1
    for v in data:
        if v<0 or v>>frombits: raise ValueError('invalid data range')
        acc=(acc<<frombits)|v; bits+=frombits
        while bits>=tobits:
            bits-=tobits; out.append((acc>>bits)&maxv)
    if pad:
        if bits: out.append((acc<<(tobits-bits))&maxv)
    elif bits>=frombits or ((acc<<(tobits-bits))&maxv): raise ValueError('invalid padding')
    return out

def segwit_address(program: bytes, version=0, hrp='bc') -> str:
    if not (0<=version<=16): raise ValueError('invalid witness version')
    spec_const = 1 if version==0 else 0x2bc830a3
    data=[version]+_convertbits(program,8,5)
    pm=_polymod(_hrp_expand(hrp)+data+[0]*6) ^ spec_const
    checksum=[(pm >> (5*(5-i))) & 31 for i in range(6)]
    return hrp+'1'+''.join(BECH32[d] for d in data+checksum)
