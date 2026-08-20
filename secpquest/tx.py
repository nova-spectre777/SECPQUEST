from __future__ import annotations

def read_varint(b:bytes,o:int):
    p=b[o]
    if p<0xfd:return p,o+1
    if p==0xfd:return int.from_bytes(b[o+1:o+3],'little'),o+3
    if p==0xfe:return int.from_bytes(b[o+1:o+5],'little'),o+5
    return int.from_bytes(b[o+1:o+9],'little'),o+9

def decode_raw_tx(hexstr:str)->dict:
    b=bytes.fromhex(hexstr.strip()); o=0
    version=int.from_bytes(b[o:o+4],'little'); o+=4
    segwit=o+1<len(b) and b[o:o+2]==b'\x00\x01'
    if segwit:o+=2
    n,o=read_varint(b,o); ins=[]
    for _ in range(n):
        prev=b[o:o+32][::-1].hex(); o+=32; vout=int.from_bytes(b[o:o+4],'little');o+=4
        ln,o=read_varint(b,o); script=b[o:o+ln].hex();o+=ln; seq=int.from_bytes(b[o:o+4],'little');o+=4
        ins.append({'prev_txid':prev,'vout':vout,'script_sig':script,'sequence':seq})
    n,o=read_varint(b,o); outs=[]
    for _ in range(n):
        val=int.from_bytes(b[o:o+8],'little');o+=8; ln,o=read_varint(b,o); script=b[o:o+ln].hex();o+=ln
        outs.append({'value_sats':val,'script_pubkey':script})
    if segwit:
        for i in range(len(ins)):
            c,o=read_varint(b,o); w=[]
            for _ in range(c): ln,o=read_varint(b,o);w.append(b[o:o+ln].hex());o+=ln
            ins[i]['witness']=w
    locktime=int.from_bytes(b[o:o+4],'little') if o+4<=len(b) else None
    return {'version':version,'segwit':segwit,'inputs':ins,'outputs':outs,'locktime':locktime}

def parse_der_signature(sighex:str)->dict:
    b=bytes.fromhex(sighex)
    if b and b[-1] in (1,2,3,0x81,0x82,0x83): b=b[:-1]
    if len(b)<8 or b[0]!=0x30: raise ValueError('not DER ECDSA')
    o=2
    if b[o]!=2: raise ValueError('missing R')
    lr=b[o+1];o+=2; r=int.from_bytes(b[o:o+lr],'big');o+=lr
    if b[o]!=2: raise ValueError('missing S')
    ls=b[o+1];o+=2; s=int.from_bytes(b[o:o+ls],'big')
    return {'r_hex':f'{r:x}','s_hex':f'{s:x}'}
