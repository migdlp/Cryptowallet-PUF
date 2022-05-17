from pypuf.simulation import XORArbiterPUF
from pypuf.io import random_inputs
from Crypto.Hash import SHA3_256


def main():

	# Número de respuestas
	N = 1000
	
	# Creamos PUF
	puf = XORArbiterPUF(n=64, k=8, seed=2, noisiness=.0)

	# creamos las N respuestas de 128bits a partir de N sets de 64 challenges de 64bits 
	# (cada challenge da una respuesta de 1 bit, por lo que resultan respuestas de 64 bits)
	for i in range(0 ,N ):
		print(i)

		# n = challenge length, N = response length
		challenges = random_inputs(n=64, N=64, seed=i)
		print("challenge: ")
		print(challenges)
		response = puf.eval(challenges)

		# transforma array de 1s y -1s a string de 0s y 1s
		response = "".join(list(map(transform_array, response)))
		responseBytes = int(response, 2).to_bytes(len(response) // 8, byteorder='big')
		print(response)

    	# HASH
		hash_obj = SHA3_256.new(responseBytes)
		responseHash = hash_obj.hexdigest()
		print(responseHash)

		# escribimos (en modo adición) cada hash
		with open('BBDD_CRPs.txt', 'a') as f:
			f.write(responseHash+"\n")
		


		

#Change every bit of the array to be a string,
# and if it's -1 change it to 0
def transform_array(bit):
    return str(bit) if bit==1 else "0"


# Start process
if __name__ == '__main__':
    main()