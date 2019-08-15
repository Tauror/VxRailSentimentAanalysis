# from Crypto.Cipher import AES
from Cryptodome.Cipher import AES
import base64
import requests
import json


headers={'origin': 'https://music.163.com',
         'referer': 'https://music.163.com/',
         'Accept':'*/*',
         'Accept-Language':'zh-CN,zh;q=0.9,en-NZ;q=0.8,en-US;q=0.7,en-CA;q=0.6,en-AU;q=0.5,en-ZA;q=0.4,en-GB;q=0.3,en;q=0.2',
         'Accept-Encoding':'gzip, deflate, br',
         'Content-Type':'application/x-www-form-urlencoded',
         'Referer':'http://music.163.com/song?id=347597',
         'Content-Length':'532',
         'Cookie':'_iuqxldmzr_=32; _ntes_nnid=93dbd20b9a941cc420d63a0d89e9dcc1,1564113004794; _ntes_nuid=93dbd20b9a941cc420d63a0d89e9dcc1; WM_NI=QOj32uFo0ATx18WnQwpM8gdFPlLN4tPPwZayHbXumpakXLY4NcbxO1ZQLivXM6HlcbOsJ0jT1%2Fgyv30QQXHDP4NPLdG5Dh3p%2BaSburTrfueXpyMJ0%2BLxgZAt34Y6OsnUaE4%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb1f67db0bda0b5d8448def8ab7d15e869a9eaeee3f82b7b9b1c763979cb786ce2af0fea7c3b92a9391a6d4b17f86b100a2d774f3e8998fd47db493f888e74e94b484afb7809490b9bbe4738cbe9896f07ca3b598addc408ebdae99ce3b9a8f848af5548fea888de26a8dad86d1e960f3f1a99af539f48f9fb9cb5094ec82b1cf7085eb8c89b27ce9bf9d83f87a98aeaa96e854b4a783abb32190a8a9bbc480f1ec97d7ce79ae8bafa6b737e2a3; WM_TID=8Ro1U585NvZBEFBQUVIpoUyxOWzACyeb; MUSIC_U=acac1f3284fd990d142448abe7f1f5773484d646d78a7de12e8eed78ae357d59ffa56ba4cc31214479ab6764a112263d616a7cd7905ba617de39c620ce8469a8; __csrf=921704bc331608ed8545053de5d026f3; JSESSIONID-WYYY=SPeQ6pj7hwQ8jPhh94doVuRweskZoguZuInrCcSBx6uCGm7HCD96K%2FmzrG06%5CaEtcN0Y8sg7CdCc6i55Jcwu5wUserUIR9eXRjGKpp2vCCs21wxbXmdg43m7wQqmH%2FY8Kx8f7yU8Bj5BbmclWbtY0v0NUqPHkIFkDqRAv1BOuW4OT5ua%3A1564132279414',	
         'Connection':'keep-alive',
         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
         }

first_param = "{rid:\"\", offset:\"0\", total:\"true\", limit:\"20\", csrf_token:\"\"}"
second_param = "010001"
third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
forth_param = "0CoJUm6Qyw8W8jud"

def get_params():
    iv = "0102030405060708"
    first_key = forth_param
    second_key = 'FFFFFFFFFFFFFFFF'
    h_encText = AES_encrypt(first_param, first_key, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText


def get_encSecKey():
    encSecKey = '386c511efcc314e6e43821aaafbf5be1b2597ea76f5dfdae440505a2649a27ed6a3c1975be8e99f609005379a3669c4ae7223b3a8ab9191f5d3fa6b7544ed7b6084c59cf6650e78b7c3c4adcd67cc47ad016893c8de5c91ca688c1b2c790a01aec4fc50608c28d24171634783fec233dfeaf98b7d301bb9728f35a5d43796bde'
    return encSecKey
    

def AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    text = bytes(text + pad * chr(pad),encoding='utf8')
    # key = bytes(key,encoding='utf8')
    # iv = bytes(iv,encoding='utf8')
    encryptor = AES.new(key, AES.MODE_CBC)
    encrypt_text = encryptor.encrypt(bytes(text,encoding='utf8'))
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text


def get_json(url, params, encSecKey):
    data = {
         "params": params,
         "encSecKey": encSecKey
    }
    response = requests.post(url, headers=headers, data=data)
    return response.content


if __name__ == "__main__":
    url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_347355?csrf_token='
    params = get_params()
    encSecKey = get_encSecKey()
    json_text = get_json(url, params, encSecKey)
    json_dict = json.loads(json_text)
    print(json_dict['total'])
    for item in json_dict['comments']:
        print(item['content'].encode('gbk', 'ignore'))