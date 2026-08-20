from __future__ import annotations
import json, mimetypes, pathlib
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from . import OWNER
from .puzzles import all_puzzles,get_puzzle
from .bitcoin import parse_scalar,pub_details_from_scalar,pubkey_details,hash160_to_addresses,script_to_addresses,wif_encode,wif_decode
from .encoding import sha256,dsha256,ripemd160,hash160,b58check_encode,b58check_decode
from .core import inv,N
from .search import verify_candidate,search,shard_range
from .tx import decode_raw_tx,parse_der_signature

ROOT=pathlib.Path(__file__).resolve().parent.parent
WEB=ROOT/'web'

class H(BaseHTTPRequestHandler):
    def _json(self,obj,status=200):
        data=json.dumps(obj,indent=2).encode(); self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
    def _body(self):
        n=int(self.headers.get('Content-Length','0')); return json.loads(self.rfile.read(n) or b'{}')
    def do_GET(self):
        u=urlparse(self.path)
        if u.path=='/api/puzzles': return self._json({'owner':OWNER,'puzzles':[p.public() for p in all_puzzles()]})
        if u.path=='/api/features': return self._json(json.loads((ROOT/'features.json').read_text()))
        if u.path=='/api/puzzle':
            try:return self._json(get_puzzle(parse_qs(u.query).get('id',[''])[0]).public())
            except Exception as e:return self._json({'error':str(e)},404)
        path=WEB/('index.html' if u.path=='/' else u.path.lstrip('/'))
        if not path.resolve().is_relative_to(WEB.resolve()) or not path.is_file(): self.send_error(404);return
        data=path.read_bytes();self.send_response(200);self.send_header('Content-Type',mimetypes.guess_type(path.name)[0] or 'application/octet-stream');self.end_headers();self.wfile.write(data)
    def do_POST(self):
        try:
            b=self._body(); p=urlparse(self.path).path
            if p=='/api/point': return self._json(pub_details_from_scalar(parse_scalar(str(b['scalar']))))
            if p=='/api/modinv': return self._json({'inverse_hex':f"{inv(parse_scalar(str(b['k'])), int(str(b.get('modulus',N)),0) if isinstance(b.get('modulus',N),str) else int(b.get('modulus',N))):x}"})
            if p=='/api/hash':
                raw=bytes.fromhex(b['data']) if b.get('mode')=='hex' else str(b['data']).encode()
                return self._json({'sha256':sha256(raw).hex(),'double_sha256':dsha256(raw).hex(),'ripemd160':ripemd160(raw).hex(),'hash160':hash160(raw).hex()})
            if p=='/api/verify': return self._json(verify_candidate(get_puzzle(str(b['puzzle'])),parse_scalar(str(b['candidate']))))
            if p=='/api/plan':
                pu=get_puzzle(str(b['puzzle'])); sh=int(b.get('shards',1)); idx=int(b.get('index',0)); s,e=shard_range(pu.start,pu.end,sh,idx)
                return self._json({'puzzle':pu.public(),'shard':{'index':idx,'shards':sh,'start_hex':f'{s:x}','end_hex':f'{e:x}','keys':e-s+1}})
            if p=='/api/search':
                pu=get_puzzle(str(b['puzzle'])); maxk=min(int(b.get('max_keys',50000)),250000)
                r=search(pu,start=int(str(b['start']),0) if b.get('start') else None,end=int(str(b['end']),0) if b.get('end') else None,max_keys=maxk)
                return self._json(r.public())
            if p=='/api/tx/decode': return self._json(decode_raw_tx(str(b['hex'])))
            if p=='/api/der': return self._json(parse_der_signature(str(b['signature'])))
            if p=='/api/hash160-addresses': return self._json(hash160_to_addresses(bytes.fromhex(str(b['hash160']))))
            if p=='/api/script-addresses': return self._json(script_to_addresses(bytes.fromhex(str(b['script']))))
            return self._json({'error':'unknown endpoint'},404)
        except Exception as e:return self._json({'error':str(e)},400)
    def log_message(self,fmt,*args): pass

def serve(host='127.0.0.1',port=8787):
    print(f'SECPQUEST web: http://{host}:{port}  | owner {OWNER}')
    ThreadingHTTPServer((host,port),H).serve_forever()
