import random
import math

def prime(n):
    sq = int(math.sqrt(n))
    if n == 2 or n == 3:
        return False
    else:
        for i in range(2,sq):
            if n%i == 0:
                return False
    return True

def gcd(a,b):
    if b == 0:
        return a 
    else:
        return gcd(b,a%b)


def keygen():
    flagp = 0
    flagq = 0
    p = -1
    q = -1
    while True:
        if flagp != 0 and flagq != 0:
            break
        if flagp == 0:
            p = random.randint(100,999)
            if prime(p):
                flagp = 1
        if  flagq == 0:
            q = random.randint(100,999)
            if prime(q) and q != p:
                flagq = 1
    n = p * q
    phi_n = (p-1) * (q-1)
    e = -1
    for i in range(2,phi_n):
        if gcd(i,phi_n) == 1:
            e = i
            break
    d = -1
    for i in range(1,n+1):
        if(e * i)%phi_n == 1:
            d = i
            break
    public_key = (e,n)
    private_key = (d,n)
    return public_key,private_key

def get_message_list(message):
    mess_block = []
    for i in message:
        x = ord(i)
        mess_block.append(x)
    return mess_block

def join_mess(mess_block):
    mess = ''
    for i in mess_block:
        mess = mess + chr(i%128)
    return mess

def encrypt(message,public_key):
    message_block = get_message_list(message)
    e = public_key[0]
    n = public_key[1]
    cipher_block = []
    for i in message_block:
        x = (i**e)%n
        cipher_block.append(x)
    cipher_text = join_mess(cipher_block)
    return cipher_text,cipher_block

def decrypt(cipher_block,private_key):
    d = private_key[0]
    n = private_key[1]
    real_block = []
    for i in cipher_block:
        x = (i**d)%n
        real_block.append(x)
    message = join_mess(real_block)
    return message

# pub,pri = keygen()
# message = 'hello'
# cipher_text,cipher_list = encrypt(message,pub)
# plain_text = decrypt(cipher_list,pri)
# print(cipher_text)
# print(cipher_list)
# print(plain_text)