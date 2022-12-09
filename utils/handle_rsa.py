import base64

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher


class RsaCrypto:
    def __init__(self, filepath):
        self.filepath = filepath

    def get_RSA_enCrypto(self, en_data: str):
        with open(self.filepath, mode='rb') as fo:
            cipher = PKCS1_cipher.new(RSA.importKey(fo.read()))
            return base64.b64encode(cipher.encrypt(en_data.encode('utf-8'))).decode()


if __name__ == '__main__':
    print(RsaCrypto('../data/mypublicKey.pem').get_RSA_enCrypto('54454987321243'))
