from __future__ import annotations
from dataclasses import dataclass

P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
GY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

@dataclass(frozen=True)
class Point:
    x: int
    y: int

G = Point(GX, GY)


def inv(a: int, m: int) -> int:
    a %= m
    if a == 0:
        raise ValueError("inverse does not exist")
    return pow(a, -1, m)


def is_on_curve(p: Point | None) -> bool:
    if p is None:
        return True
    return (p.y * p.y - (p.x * p.x * p.x + 7)) % P == 0


def add(a: Point | None, b: Point | None) -> Point | None:
    if a is None: return b
    if b is None: return a
    if a.x == b.x and (a.y + b.y) % P == 0: return None
    if a == b:
        if a.y == 0: return None
        lam = (3 * a.x * a.x) * inv(2 * a.y, P) % P
    else:
        lam = (b.y - a.y) * inv(b.x - a.x, P) % P
    x = (lam * lam - a.x - b.x) % P
    y = (lam * (a.x - x) - a.y) % P
    r = Point(x, y)
    if not is_on_curve(r):
        raise ArithmeticError("point addition produced invalid point")
    return r


def mul(k: int, p: Point = G) -> Point | None:
    k %= N
    if k == 0: return None
    out = None
    cur = p
    while k:
        if k & 1: out = add(out, cur)
        cur = add(cur, cur)
        k >>= 1
    return out


def compress(p: Point) -> bytes:
    return bytes([2 | (p.y & 1)]) + p.x.to_bytes(32, "big")


def uncompress(p: Point) -> bytes:
    return b"\x04" + p.x.to_bytes(32, "big") + p.y.to_bytes(32, "big")


def decompress(data: bytes) -> Point:
    if len(data) == 65 and data[0] == 4:
        p = Point(int.from_bytes(data[1:33], 'big'), int.from_bytes(data[33:], 'big'))
        if not is_on_curve(p): raise ValueError("point is not on secp256k1")
        return p
    if len(data) != 33 or data[0] not in (2,3):
        raise ValueError("expected compressed/uncompressed secp256k1 public key")
    x = int.from_bytes(data[1:], 'big')
    y2 = (pow(x,3,P)+7) % P
    y = pow(y2, (P+1)//4, P)
    if (y & 1) != (data[0] & 1): y = P-y
    p = Point(x,y)
    if not is_on_curve(p): raise ValueError("point is not on secp256k1")
    return p
