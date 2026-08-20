import unittest
from secpquest.puzzles import get_puzzle
from secpquest.search import shard_range,verify_candidate,search
class T(unittest.TestCase):
    def test_shards_cover(self):
        parts=[shard_range(10,29,3,i) for i in range(3)]
        vals=[]
        for a,b in parts:vals.extend(range(a,b+1))
        self.assertEqual(vals,list(range(10,30)))
    def test_synthetic_verify(self): self.assertTrue(verify_candidate(get_puzzle('synthetic-20'),0xabcde)['match'])
    def test_synthetic_search(self):
        p=get_puzzle('synthetic-20');r=search(p,start=0xabcd0,max_keys=32,checkpoint_every=4)
        self.assertTrue(r.found);self.assertEqual(r.key,0xabcde)
if __name__=='__main__':unittest.main()
