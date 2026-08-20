import unittest
from secpquest.core import G,N,mul,compress,decompress,inv,is_on_curve
from secpquest.bitcoin import pub_details_from_scalar,wif_encode,wif_decode
from secpquest.tx import parse_der_signature
class T(unittest.TestCase):
    def test_generator(self): self.assertEqual(mul(1),G)
    def test_order(self): self.assertIsNone(mul(N))
    def test_roundtrip_pub(self):
        p=mul(123456);self.assertEqual(decompress(compress(p)),p);self.assertTrue(is_on_curve(p))
    def test_inverse(self): self.assertEqual((7*inv(7,N))%N,1)
    def test_known_key_one(self): self.assertEqual(pub_details_from_scalar(1)['p2pkh_compressed'],'1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH')
    def test_wif(self):
        w=wif_encode(1,True);k,c,t=wif_decode(w);self.assertEqual(k,1);self.assertTrue(c);self.assertFalse(t)
    def test_der_parser(self):
        d=parse_der_signature('3006020101020104')
        self.assertEqual(d,{'r_hex':'1','s_hex':'4'})
if __name__=='__main__':unittest.main()
