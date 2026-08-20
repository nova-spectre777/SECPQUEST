from __future__ import annotations
import json, pathlib
from dataclasses import dataclass, asdict

ROOT=pathlib.Path(__file__).resolve().parent.parent
MANIFEST_DIR=ROOT/'manifests'

@dataclass(frozen=True)
class Puzzle:
    id: str
    title: str
    kind: str
    network: str
    start: int
    end: int
    target_address: str | None
    target_pubkey: str | None
    source_url: str | None
    notes: str

    @property
    def size(self): return self.end-self.start+1
    @property
    def bits(self): return self.size.bit_length()-1 if self.size and self.size&(self.size-1)==0 else self.size.bit_length()
    def public(self):
        d=asdict(self); d.update(size=self.size,bits=self.bits,start_hex=f'{self.start:x}',end_hex=f'{self.end:x}'); return d


def _load(path:pathlib.Path)->Puzzle:
    d=json.loads(path.read_text())
    return Puzzle(id=d['id'], title=d['title'], kind=d['kind'], network=d.get('network','mainnet'),
                  start=int(d['start'],0), end=int(d['end'],0), target_address=d.get('target_address'),
                  target_pubkey=d.get('target_pubkey'), source_url=d.get('source_url'), notes=d.get('notes',''))


def all_puzzles()->list[Puzzle]: return [_load(p) for p in sorted(MANIFEST_DIR.glob('*.json'))]
def get_puzzle(pid:str)->Puzzle:
    for p in all_puzzles():
        if p.id==pid or p.title.lower()==pid.lower(): return p
    raise KeyError(f'unknown built-in puzzle: {pid}')

def search_allowed(p:Puzzle)->bool: return p.kind in {'public_challenge','synthetic'}
