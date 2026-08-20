from __future__ import annotations
import argparse,json
from . import OWNER
from .core import inv,N
from .encoding import sha256,dsha256,ripemd160,hash160,b58check_encode,b58check_decode
from .bitcoin import parse_scalar,pub_details_from_scalar,pubkey_details,wif_encode,wif_decode,hash160_to_addresses,script_to_addresses
from .puzzles import all_puzzles,get_puzzle
from .search import shard_range,verify_candidate,search
from .tx import decode_raw_tx,parse_der_signature
from .web import serve

def emit(x): print(json.dumps(x,indent=2,sort_keys=True))
def main(argv=None):
    ap=argparse.ArgumentParser(prog='secpquest',description='SECPQUEST / RANGE-Ω — public Bitcoin puzzle mathematics engine')
    ap.add_argument('--owner',action='version',version=OWNER)
    sp=ap.add_subparsers(dest='cmd',required=True)
    sp.add_parser('list-puzzles')
    sp.add_parser('features')
    p=sp.add_parser('show');p.add_argument('puzzle')
    p=sp.add_parser('point');p.add_argument('scalar')
    p=sp.add_parser('pubkey');p.add_argument('pubkey_hex')
    p=sp.add_parser('modinv');p.add_argument('k');p.add_argument('--modulus',default=hex(N))
    p=sp.add_parser('hash');p.add_argument('data');p.add_argument('--hex',action='store_true')
    p=sp.add_parser('wif-encode');p.add_argument('scalar');p.add_argument('--uncompressed',action='store_true')
    p=sp.add_parser('wif-decode');p.add_argument('wif')
    p=sp.add_parser('hash160-addresses');p.add_argument('hash160')
    p=sp.add_parser('script-addresses');p.add_argument('script')
    p=sp.add_parser('tx-decode');p.add_argument('hex')
    p=sp.add_parser('der');p.add_argument('signature')
    p=sp.add_parser('plan');p.add_argument('puzzle');p.add_argument('--shards',type=int,default=1);p.add_argument('--index',type=int,default=0)
    p=sp.add_parser('verify');p.add_argument('puzzle');p.add_argument('candidate')
    p=sp.add_parser('search');p.add_argument('puzzle');p.add_argument('--start');p.add_argument('--end');p.add_argument('--max-keys',type=int,default=100000);p.add_argument('--shards',type=int);p.add_argument('--index',type=int,default=0)
    p=sp.add_parser('web');p.add_argument('--host',default='127.0.0.1');p.add_argument('--port',type=int,default=8787)
    a=ap.parse_args(argv)
    if a.cmd=='list-puzzles': return emit([p.public() for p in all_puzzles()])
    if a.cmd=='features':
        import pathlib
        return emit(json.loads((pathlib.Path(__file__).resolve().parent.parent/'features.json').read_text()))
    if a.cmd=='show': return emit(get_puzzle(a.puzzle).public())
    if a.cmd=='point': return emit(pub_details_from_scalar(parse_scalar(a.scalar)))
    if a.cmd=='pubkey': return emit(pubkey_details(a.pubkey_hex))
    if a.cmd=='modinv':
        k=parse_scalar(a.k);m=int(a.modulus,0);return emit({'k_hex':f'{k:x}','modulus_hex':f'{m:x}','inverse_hex':f'{inv(k,m):x}'})
    if a.cmd=='hash':
        b=bytes.fromhex(a.data) if a.hex else a.data.encode();return emit({'sha256':sha256(b).hex(),'double_sha256':dsha256(b).hex(),'ripemd160':ripemd160(b).hex(),'hash160':hash160(b).hex()})
    if a.cmd=='wif-encode':
        k=parse_scalar(a.scalar);return emit({'wif':wif_encode(k,not a.uncompressed),'compressed':not a.uncompressed})
    if a.cmd=='wif-decode':
        k,c,t=wif_decode(a.wif);return emit({'scalar_hex':f'{k:064x}','compressed':c,'testnet':t})
    if a.cmd=='hash160-addresses': return emit(hash160_to_addresses(bytes.fromhex(a.hash160)))
    if a.cmd=='script-addresses': return emit(script_to_addresses(bytes.fromhex(a.script)))
    if a.cmd=='tx-decode': return emit(decode_raw_tx(a.hex))
    if a.cmd=='der': return emit(parse_der_signature(a.signature))
    if a.cmd=='plan':
        pu=get_puzzle(a.puzzle);s,e=shard_range(pu.start,pu.end,a.shards,a.index);return emit({'puzzle':pu.id,'start_hex':f'{s:x}','end_hex':f'{e:x}','keys':e-s+1,'shards':a.shards,'index':a.index})
    if a.cmd=='verify': return emit(verify_candidate(get_puzzle(a.puzzle),parse_scalar(a.candidate)))
    if a.cmd=='search':
        pu=get_puzzle(a.puzzle);s=int(a.start,0) if a.start else None;e=int(a.end,0) if a.end else None
        if a.shards:
            s,e=shard_range(pu.start,pu.end,a.shards,a.index)
        return emit(search(pu,s,e,a.max_keys).public())
    if a.cmd=='web': return serve(a.host,a.port)
if __name__=='__main__': main()
