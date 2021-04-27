import secrets

alphabet = '0123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'


def encode(num):
    return ''.join([alphabet[secrets.randbelow(len(alphabet))] for i in range(num)])


def generate_short_uid():
    return encode(8)
