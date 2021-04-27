import secrets

alphabet = '0123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'


def random(num):
    return ''.join([alphabet[secrets.randbelow(len(alphabet))] for i in range(num)])
