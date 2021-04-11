import math
import random


min = 7427658739644928
max = 9007199254740992

def randomInt(min, max) :
  return math.floor(random.random() * (max - min)) + min



alphabet = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'

def encode(num):
    encode = ''
    base_count = len(alphabet)
    while (num >= base_count):
        tmp = num / base_count
        mod = num - base_count * tmp
        encode = alphabet[mod] + encode
        num = tmp

    if (num):
        encode = alphabet[tmp] + encode
    return encode

def generateShortUid():
  return encode(randomInt(min, max))
