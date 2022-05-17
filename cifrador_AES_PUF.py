#!/usr/bin/env python
import sys
import os
from pypuf.simulation import XORArbiterPUF
from pypuf.io import random_inputs
#Using cryptodome library
from Crypto.Cipher import AES

def main():

    codification = 'cp1252'
    walletName = "Wallet_1"
    directoryName = "./BBDD_wallets/"

    # Se evaluan 256 challenges en el simulador PUF,
    # devuelve array de 256 bits
    puf = XORArbiterPUF(n=64, k=8, seed=1, noisiness=.0)
    challenges = random_inputs(n=64, N=256, seed=1)
    response = puf.eval(challenges)


    #Transforma las respuestas a bytes para poder pasarlo por el AES
    bitsArray = list(map(transform_array, response))
    bitsString = "".join(bitsArray)
    responseBytes = int(bitsString, 2).to_bytes(len(bitsString) // 8, byteorder='big')

    # Si trae dos argumentos -> Encripta
    if( len(sys.argv) > 2 ):
        # recoge el primer parametro que le pasamos al script
        # (la llave de la cartera)
        walletKey = sys.argv[1]

        # recoge el segundo parámetro que le pasamos al script
        # (el nombre de la cartera)
        walletName = sys.argv[2]

        
        # ciframos walletKey con response de la PUF en formato byte 
        nonce, encryptedKey, tag = encrypt(responseBytes, walletKey.encode(codification))

        # y guardamos llave cifrada
        # No es necesario guardar challenge porque son reproducibles
        os.makedirs(os.path.dirname(directoryName), exist_ok=True)
        with open(directoryName + walletName + '.bin', 'wb') as f:
            f.write(nonce)
            f.write(tag)
            f.write(encryptedKey)

        exit()

    # Si solo trae un argumento -> Desencripta
    elif ( len(sys.argv) > 1 ):
        
        # recoge el segundo parámetro que le pasamos al script, en este caso:
        # (el nombre de la cartera)
        walletName = sys.argv[1]
        
        # recogemos llave cifrada y challenges del fichero
        os.makedirs(os.path.dirname(directoryName), exist_ok=True)
        with open(directoryName+ walletName + '.bin', 'rb') as f:          
            nonce = f.readline(16)
            f.seek(16)
            tag = f.readline(16)
            f.seek(32)
            encryptedKey = f.readline()
        
        # la desciframos
        llaveDescifrada = decrypt(responseBytes, encryptedKey, tag, nonce)

        exit(llaveDescifrada.decode(codification))


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


# Start process
if __name__ == '__main__':
    main()