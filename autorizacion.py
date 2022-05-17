from pypuf.simulation import XORArbiterPUF
from pypuf.io import random_inputs
from Crypto.Hash import SHA3_256
import random

def main():

	

	# Número de respuestas totales
	N = 1000
	# Número de respuestas aleatorias
	N_random = 250

	randomChallenges = [ ]
 	
	for i in range (N_random):
		randomChallenges.append(random.randint(0, N-1))
	

	# Creamos PUF
	puf = XORArbiterPUF(n=64, k=8, seed=2, noisiness=.0)

	try:
		# Leemos los hashes y los guardamos en realHashes
		realHashes = ""
		with open('BBDD_CRPs.txt', 'r') as f:
			realHashes = f.readlines()
	except:
		# Recoge excepción FileNotFoundError: [Errno 2] No such file or directory: 'BBDD_CRPs.txt'
		# Si no existe el fichero significa que no esta emparejado, devolvemos un 2
		exit(2)

	# Inicializamos autorized a 0 (autorizado )
	authorized = 0

	# creamos los N respuestas de 128bits a partir de N challenges de 64bits
	for i in randomChallenges:

		# n = challenge length, N = response length
		challenges = random_inputs(n=64, N=64, seed=i)
		response = puf.eval(challenges)

		# transforma array de 1s y -1s a string de 0s y 1s
		response = "".join(list(map(transform_array, response)))
		responseBytes = int(response, 2).to_bytes(len(response) // 8, byteorder='big')

    	# HASH
		hash_obj = SHA3_256.new(responseBytes)
		responseHash = hash_obj.hexdigest()

		# Comparamos cada hash, si alguno fuera distinto, no se autoriza al dispositivo
		# Se usa [:-1] para eliminar el salto de linea del fichero ("\n")
		if (responseHash != realHashes[i][:-1]):
			# authized a 1 (no autorizado)
			authorized = 1

	exit(authorized)

	
#Change every bit of the array to be a string,
# and if it's -1 change it to 0
def transform_array(bit):
    return str(bit) if bit==1 else "0"


# Start process
if __name__ == '__main__':
    main()