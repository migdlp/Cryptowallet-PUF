import sys
import os
from pypuf.simulation import XORBistableRingPUF
from pypuf.io import random_inputs
from numpy.random import default_rng
from Crypto.Cipher import AES


# Encripta con la clave generada por la PUF simulada
def PUFCipher( walletName, walletKey):

    codification = 'cp1252'

    directoryName = "./BBDD_wallets/"

    KeyInBytes = PUFKeyGenerator()
        
    # ciframos walletKey con response de la PUF en formato byte 
    nonce, encryptedKey, tag = encrypt(KeyInBytes, walletKey.encode(codification))

    # y guardamos llave cifrada
    # No es necesario guardar challenge porque son reproducibles
    os.makedirs(os.path.dirname(directoryName), exist_ok=True)
    with open(directoryName + walletName + '.bin', 'wb') as f:
        f.write(nonce)
        f.write(tag)
        f.write(encryptedKey)


# Desencripta con la clave generada por la PUF simulada
def PUFDecipher(walletName):
    codification = 'cp1252'

    directoryName = "./BBDD_wallets/"

    KeyInBytes = PUFKeyGenerator()
    # recogemos llave cifrada y challenges del fichero
    os.makedirs(os.path.dirname(directoryName), exist_ok=True)
    with open(directoryName+ walletName + '.bin', 'rb') as f:          
        nonce = f.readline(16)
        f.seek(16)
        tag = f.readline(16)
        f.seek(32)
        encryptedKey = f.readline()
    
    # la desciframos
    DecryptedKey = decrypt(KeyInBytes, encryptedKey, tag, nonce)

    return(DecryptedKey.decode(codification))

# Genera la clave de 256 bits mediante el simulador PUF
def PUFKeyGenerator():

    # Se evaluan 256 challenges en el simulador PUF,
    # devuelve array de 256 bits
    k, n = 8, 64
    weights = default_rng(1).normal(size=(k, n+1))
    puf = XORBistableRingPUF(n=64, k=8,  weights=weights)
    challenges = random_inputs(n=64, N=256, seed=1)
    response = puf.eval(challenges)

    #Transforma las respuestas a bytes para poder pasarlo por el AES
    bitsArray = list(map(transform_array, response))
    bitsString = "".join(bitsArray)
    responseBytes = int(bitsString, 2).to_bytes(len(bitsString) // 8, byteorder='big')
    return responseBytes


def encrypt(key, data):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return cipher.nonce, ciphertext, tag


def decrypt(key, data, tag, nonce):

    cipher = AES.new(key, AES.MODE_EAX, nonce)
    return cipher.decrypt_and_verify(data, tag)


#Change every bit of the array to be a string,
# and if it's -1 change it to 0
def transform_array(bit):
    return str(bit) if bit==1 else "0"
