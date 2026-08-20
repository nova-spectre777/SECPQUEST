from __future__ import annotations
from .core import N, Point, mul, compress, uncompress, decompress
from .encoding import hash160,b58check_encode,b58check_decode,segwit_address,sha256


def parse_scalar(text: str) -> int:
    s=text.strip().lower()
    if s.startswith('0x'): v=int(s,16)
    elif any(c in 'abcdef' for c in s): v=int(s,16)
    else: v=int(s,10)
    if not 1 <= v < N: raise ValueError('scalar must satisfy 1 <= k < secp256k1 n')
    return v


def p2pkh_from_pub(pub: bytes, testnet=False) -> str:
    return b58check_encode(bytes([0x6f if testnet else 0x00])+hash160(pub))


def p2wpkh_from_pub(pub: bytes, testnet=False) -> str:
    return segwit_address(hash160(pub),0,'tb' if testnet else 'bc')


def pub_details_from_scalar(k: int) -> dict:
    p=mul(k)
    if p is None: raise ValueError('point at infinity')
    c,u=compress(p),uncompress(p)
    return {
        'scalar_hex': f'{k:064x}',
        'x_hex': f'{p.x:064x}', 'y_hex': f'{p.y:064x}',
        'compressed_pubkey': c.hex(), 'uncompressed_pubkey': u.hex(),
        'p2pkh_compressed': p2pkh_from_pub(c),
        'p2pkh_uncompressed': p2pkh_from_pub(u),
        'p2wpkh': p2wpkh_from_pub(c),
    }


def wif_encode(k:int, compressed=True, testnet=False)->str:
    payload=bytes([0xef if testnet else 0x80])+k.to_bytes(32,'big')+(b'\x01' if compressed else b'')
    return b58check_encode(payload)


def wif_decode(s:str)->tuple[int,bool,bool]:
    p=b58check_decode(s)
    if p[0] not in (0x80,0xef): raise ValueError('not a Bitcoin WIF')
    testnet=p[0]==0xef; body=p[1:]; compressed=False
    if len(body)==33 and body[-1]==1: compressed=True; body=body[:-1]
    if len(body)!=32: raise ValueError('invalid WIF length')
    k=int.from_bytes(body,'big')
    if not 1<=k<N: raise ValueError('WIF scalar out of range')
    return k,compressed,testnet


def pubkey_details(pubhex:str)->dict:
    p=decompress(bytes.fromhex(pubhex))
    c,u=compress(p),uncompress(p)
    return {'x_hex':f'{p.x:064x}','y_hex':f'{p.y:064x}','compressed_pubkey':c.hex(),'uncompressed_pubkey':u.hex(),
            'p2pkh_compressed':p2pkh_from_pub(c),'p2pkh_uncompressed':p2pkh_from_pub(u),'p2wpkh':p2wpkh_from_pub(c)}


def hash160_to_addresses(h:bytes)->dict:
    if len(h)!=20: raise ValueError('HASH160 must be 20 bytes')
    return {'p2pkh': b58check_encode(b'\x00'+h), 'p2sh': b58check_encode(b'\x05'+h), 'p2wpkh': segwit_address(h,0,'bc')}


def script_to_addresses(script:bytes)->dict:
    return {'p2sh': b58check_encode(b'\x05'+hash160(script)), 'p2wsh': segwit_address(sha256(script),0,'bc')}
