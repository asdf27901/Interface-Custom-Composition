# ================
# 2022/12/11 21:02
# handle_rsa.PY
# author:Meffa
# ================
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_v1_5 as PKCS1_cipher


class RsaCrypto:
    def __init__(self, filepath):
        self.filepath = filepath

    def get_RSA_enCrypto(self, en_data: str):
        with open(self.filepath, mode='rb') as fo:
            cipher_text = PKCS1_cipher.new(RSA.importKey(fo.read())).encrypt(en_data.encode('utf-8'))
            return base64.b64encode(cipher_text).decode()


if __name__ == '__main__':
    print(RsaCrypto('../data/public.pem').get_RSA_enCrypto('123'))
