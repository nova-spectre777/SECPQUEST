from __future__ import annotations
from collections import Counter

def nonce_observations(rows:list[tuple[int,int,int]])->dict:
    """Defensive statistics only. Does not recover arbitrary private keys."""
    if not rows: return {'count':0}
    rs=[r for r,_,_ in rows]
    repeats=[f'{r:x}' for r,c in Counter(rs).items() if c>1]
    bitlens=[r.bit_length() for r in rs]
    leading_zero_bits=[256-b for b in bitlens]
    return {'count':len(rows),'repeated_r':repeats,'min_r_bits':min(bitlens),'max_r_bits':max(bitlens),
            'avg_r_bits':sum(bitlens)/len(bitlens),'max_leading_zero_bits':max(leading_zero_bits),
            'warning':'R bit length alone does not prove nonce k is short; treat this as a statistical signal only.'}
