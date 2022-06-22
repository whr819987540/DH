from pickle import NONE
from random import randint


def generate_big_prime():
    """
    生成一个随机大素数
    """
    return 13


def get_big_prime_generator(p: int):
    """
    生成大素数的原根
    """
    a = p - 1
    while a >= 2:
        flag = 1
        while flag != p:
            if (a ** flag) % p == 1:
                break
            flag += 1
        if flag == (p - 1):
            return a
        a -= 1


def get_private_key(p: int):
    """
    私钥即为[1,p-1]之间的随机数
    """
    return randint(1, p-1)


def get_public_key(p: int, g: int, private_key: int):
    """
    根据大素数p、原根g、私钥private_key生成公钥
    private_key = g^pk mod p
    """
    return (g ** private_key) % p


def get_S(p: int, local_private_key: int, remote_public_key: int):
    """
    根据大素数p、本地私钥、远程公钥生成对称秘钥S
    """
    return (remote_public_key ** local_private_key) % p


def AES256_GCM_encrypt():
    """
    AES256加密，GCM模式
    """
    return "data"


def AES256_GCM_decrypt():
    """
    AES256加解密，GCM模式
    """
    return None


if __name__ == "__main__":
    print(get_big_prime_generator(197))
