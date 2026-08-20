from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
import time
from .core import G, add, mul, compress, uncompress
from .bitcoin import p2pkh_from_pub
from .puzzles import Puzzle, search_allowed

@dataclass
class SearchResult:
    found: bool
    key: int|None
    tested: int
    start: int
    end: int
    elapsed_s: float
    checkpoints: int
    work_root: str

    def public(self):
        return {'found':self.found,'key_hex':f'{self.key:064x}' if self.key else None,'tested':self.tested,
                'start_hex':f'{self.start:x}','end_hex':f'{self.end:x}','elapsed_s':round(self.elapsed_s,6),
                'keys_per_s':round(self.tested/self.elapsed_s,2) if self.elapsed_s else None,
                'checkpoints':self.checkpoints,'work_root':self.work_root}

def shard_range(start:int,end:int,shards:int,index:int)->tuple[int,int]:
    if shards<1 or not 0<=index<shards: raise ValueError('invalid shard settings')
    size=end-start+1; base=size//shards; rem=size%shards
    s=start + index*base + min(index,rem)
    e=s+base-1+(1 if index<rem else 0)
    return s,e

def _merkle_root(leaves:list[bytes])->str:
    if not leaves: return sha256(b'').hexdigest()
    layer=[sha256(x).digest() for x in leaves]
    while len(layer)>1:
        if len(layer)%2: layer.append(layer[-1])
        layer=[sha256(layer[i]+layer[i+1]).digest() for i in range(0,len(layer),2)]
    return layer[0].hex()

def verify_candidate(puzzle:Puzzle,k:int)->dict:
    if not search_allowed(puzzle): raise PermissionError('manifest is not approved for search')
    if not puzzle.start<=k<=puzzle.end: return {'match':False,'reason':'outside declared puzzle range'}
    pt=mul(k); c=compress(pt); u=uncompress(pt)
    candidates={'p2pkh_compressed':p2pkh_from_pub(c),'p2pkh_uncompressed':p2pkh_from_pub(u)}
    if puzzle.target_address:
        ok=puzzle.target_address in candidates.values()
        return {'match':ok,'addresses':candidates}
    if puzzle.target_pubkey:
        ok=puzzle.target_pubkey.lower() in {c.hex().lower(),u.hex().lower()}
        return {'match':ok,'addresses':candidates}
    return {'match':False,'reason':'manifest has no target'}

def search(puzzle:Puzzle,start:int|None=None,end:int|None=None,max_keys:int=100000,checkpoint_every:int=4096)->SearchResult:
    if not search_allowed(puzzle): raise PermissionError('only built-in public challenges and synthetic manifests are searchable')
    s=max(puzzle.start, start if start is not None else puzzle.start)
    e=min(puzzle.end, end if end is not None else puzzle.end)
    if s>e: raise ValueError('empty search range')
    if max_keys<1: raise ValueError('max_keys must be positive')
    e=min(e,s+max_keys-1)
    t0=time.perf_counter(); tested=0; leaves=[]; found=None
    pt=mul(s)
    k=s
    while k<=e:
        c=compress(pt); u=uncompress(pt)
        tested+=1
        if puzzle.target_address and puzzle.target_address in (p2pkh_from_pub(c),p2pkh_from_pub(u)):
            found=k; leaves.append(f'{k:x}:{c.hex()}:FOUND'.encode()); break
        if puzzle.target_pubkey and puzzle.target_pubkey.lower() in (c.hex().lower(),u.hex().lower()):
            found=k; leaves.append(f'{k:x}:{c.hex()}:FOUND'.encode()); break
        if tested==1 or tested%checkpoint_every==0:
            leaves.append(f'{k:x}:{c.hex()}'.encode())
        pt=add(pt,G); k+=1
    elapsed=time.perf_counter()-t0
    return SearchResult(bool(found),found,tested,s,(found if found else min(e,s+tested-1)),elapsed,len(leaves),_merkle_root(leaves))
